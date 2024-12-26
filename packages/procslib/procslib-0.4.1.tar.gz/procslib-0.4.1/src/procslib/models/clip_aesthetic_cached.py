import os
import warnings
from pathlib import Path
from typing import List, Tuple

import h5py
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from huggingface_hub import hf_hub_download
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
from transformers import CLIPModel, CLIPProcessor

from .base_inference import BaseImageInference, custom_collate

# ======== Custom Dataset


class ClipImageDataset(Dataset):
    """A simple dataset that:
    - Takes a list of image paths (absolute or otherwise).
    - Uses a CLIPProcessor to convert each image to pixel_values (shape [3,H,W]).
    """

    def __init__(self, image_paths: List[str], processor: CLIPProcessor):
        self.image_paths = image_paths
        self.processor = processor

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        try:
            image = Image.open(path).convert("RGB")
            # Convert the PIL Image to [3, H, W] using the processor's image transform
            pixel_values = self.processor.image_processor(image).pixel_values[0]
            return torch.from_numpy(pixel_values), path
        except Exception as e:
            warnings.warn(f"Error loading image {path}: {e}")
            # Return a zero-tensor if loading fails
            zero_tensor = torch.zeros(3, 224, 224, dtype=torch.float32)
            return zero_tensor, path


# ======== Helpers


def sanitize_key(path: str) -> str:
    """HDF5 treats '/' as nested groups, so we replace them (and backslashes)
    with a harmless token. This yields a single-level key.
    """
    return path.replace("\\", "__").replace("/", "__")


def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def tensor_to_float(tensor, precision=5):
    # Move tensor to CPU if it's on GPU, convert to numpy array, and get the first element
    value = tensor.cpu().detach().numpy().item()

    # Format the value to a float with specified precision
    formatted_value = round(value, precision)

    return formatted_value


class MLP(nn.Module):
    def __init__(self, input_size, xcol="emb", ycol="avg_rating"):
        super().__init__()
        self.input_size = input_size
        self.xcol = xcol
        self.ycol = ycol
        self.layers = nn.Sequential(
            nn.Linear(self.input_size, 1024),
            # nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(1024, 128),
            # nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            # nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(64, 16),
            # nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x):
        return self.layers(x)

    def training_step(self, batch, batch_idx):
        x = batch[self.xcol]
        y = batch[self.ycol].reshape(-1, 1)
        x_hat = self.layers(x)
        loss = F.mse_loss(x_hat, y)
        return loss

    def validation_step(self, batch, batch_idx):
        x = batch[self.xcol]
        y = batch[self.ycol].reshape(-1, 1)
        x_hat = self.layers(x)
        loss = F.mse_loss(x_hat, y)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer


def get_mlp_model(input_source):
    """Load a pre-trained MLP model from either a local path or a huggingface hub repo id.
    MLP is in the format of https://github.com/christophschuhmann/improved-aesthetic-predictor

    :param input_source: either a local path to a model, or a huggingface hub repo id
        (e.g. "openai/clip-vit-large-patch14")
    :return:
    """
    try:
        print(f"Attempting to load model from Hugging Face Hub: {input_source}")
        model_path = Path(hf_hub_download(repo_id=input_source, filename="model.pth"))
    except Exception as e:
        print(f"Failed to load from Hugging Face Hub, trying local path. Error: {e}")
        model_path = input_source

    model = MLP(768)
    s = torch.load(model_path, map_location=torch.device("cuda"))
    model.load_state_dict(s)
    model.to("cuda")
    model.eval()
    return model


# ======== Inference Class


class CachedClipAestheticInference(BaseImageInference):
    """A model pipeline that:
      1) Loads or computes CLIP image embeddings,
      2) Optionally applies MLP(s) for final aesthetic scores,
      3) Caches embeddings in HDF5 to skip re-computation.

    We override infer_many to do a custom pipeline:
      - load from HDF5 if cached,
      - compute new embeddings for uncached images,
      - produce final DataFrame with normal (original) paths.
    """

    def __init__(
        self,
        prompts_list: List[str],
        mlp_configs: List[Tuple[torch.nn.Module, str]],
        h5_path: str,
        model_id: str = "openai/clip-vit-large-patch14",
        device: str = "cuda",
        batch_size: int = 32,
        num_workers: int = 4,
    ):
        """Args:
        prompts_list: list of text prompts for CLIP similarity scoring.
        mlp_configs: List of (mlp_model, key_name) for additional MLP-based scores.
        h5_path: Path to the HDF5 file for caching embeddings.
        model_id: HF model id, e.g. "openai/clip-vit-large-patch14".
        device: "cpu" or "cuda".
        batch_size: batch size for DataLoader in infer_many.
        num_workers: num of workers for image loading.
        """
        super().__init__(device=device, batch_size=batch_size)
        self.prompts_list = prompts_list
        self.mlp_configs = mlp_configs
        self.h5_path = h5_path
        self.model_id = model_id
        self.num_workers = num_workers

        self.image_features = {}  # in-memory cache: {original_path -> np.array embedding}

        self._load_model()  # ignoring checkpoint_path arg
        self._prepare_text_embeddings()

    # -----------------------------
    # Overriding / implementing ABC methods
    # -----------------------------

    def _load_model(self, checkpoint_path: str = None):
        """Load CLIP model + processor from Hugging Face, onto self.device."""
        self.clip_model = CLIPModel.from_pretrained(self.model_id).to(self.device)
        self.clip_processor = CLIPProcessor.from_pretrained(self.model_id)
        self.clip_model.eval()

    def _preprocess_image(self, pil_image: Image.Image) -> torch.Tensor:
        """Return a dummy [3,224,224]. We won't use base infer_many for real logic,
        we do a custom pipeline.
        """
        return torch.zeros(3, 224, 224)

    def _postprocess_output(self, logits: torch.Tensor):
        """Not used in the custom pipeline. Just return zeros."""
        return [0.0] * logits.shape[0]

    # -----------------------------
    # Additional steps for CLIP + MLP logic
    # -----------------------------

    def _prepare_text_embeddings(self):
        """Precompute text embeddings for the prompts_list, store on GPU for quick multiply."""
        old_env = os.environ.get("TOKENIZERS_PARALLELISM", None)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

        with torch.no_grad():
            inputs = self.clip_processor.tokenizer(
                self.prompts_list,
                padding=True,
                return_tensors="pt",
            ).to(self.device)
            text_emb = self.clip_model.get_text_features(**inputs)
            text_emb = text_emb / text_emb.norm(p=2, dim=-1, keepdim=True)
            self.text_features = text_emb  # shape [num_prompts, D]

        # Restore environment var
        if old_env is None:
            del os.environ["TOKENIZERS_PARALLELISM"]
        else:
            os.environ["TOKENIZERS_PARALLELISM"] = old_env

    def _load_cached_embeddings(self, image_paths: List[str]) -> List[str]:
        """For each path in image_paths, if HDF5 has an entry, load it into self.image_features.
        Return a list of paths that are missing in the cache (need processing).
        """
        to_process = []
        if os.path.exists(self.h5_path):
            with h5py.File(self.h5_path, "r") as h5f:
                for p in image_paths:
                    key = sanitize_key(p)
                    if key in h5f:
                        self.image_features[p] = h5f[key][()]  # stored as np.array
                    else:
                        to_process.append(p)
        else:
            # If there's no HDF5, all paths are new
            to_process = image_paths
            # Ensure parent dirs for h5 exist
            os.makedirs(os.path.dirname(self.h5_path) or ".", exist_ok=True)
        return to_process

    def _compute_embeddings_for(self, paths_to_process: List[str]):
        """Load images for these paths, run CLIP image embedding,
        store them in memory and in the HDF5 file.
        """
        if not paths_to_process:
            return

        dataset = ClipImageDataset(paths_to_process, self.clip_processor)
        loader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            collate_fn=custom_collate,
        )
        with torch.no_grad(), h5py.File(self.h5_path, "a") as h5f:
            for batch in tqdm(loader, desc="Computing CLIP embeddings"):
                if batch is None:
                    continue
                images, batch_paths = batch
                images = images.to(self.device)
                emb = self.clip_model.get_image_features(pixel_values=images)
                emb = emb / emb.norm(p=2, dim=-1, keepdim=True)  # shape [B, D]

                for path, vec in zip(batch_paths, emb):
                    arr = vec.cpu().numpy()
                    self.image_features[path] = arr
                    key = sanitize_key(path)
                    if key not in h5f:
                        h5f.create_dataset(key, data=arr)

    def _compute_scores_from_features(self) -> dict:
        """For each path's embedding in self.image_features, compute:
          - CLIP similarity to each prompt,
          - MLP-based scores if mlp_configs are given.
        Return { path: {...scores...} }.
        """
        results = {}
        scale = self.clip_model.logit_scale.exp()
        with torch.no_grad():
            for path, emb_np in tqdm(self.image_features.items(), desc="Computing final scores"):
                emb_tensor = torch.tensor(emb_np, device=self.device).unsqueeze(0)  # [1, D]

                # CLIP similarity
                clip_scores_tensor = (emb_tensor @ self.text_features.t()) * scale
                clip_scores = clip_scores_tensor.squeeze(0).cpu().numpy()
                clip_scores_dict = {prompt: float(sc) for prompt, sc in zip(self.prompts_list, clip_scores)}

                # MLP scores
                mlp_results = {}
                emb_norm_np = normalized(emb_tensor.cpu().numpy())
                emb_norm_tensor = torch.from_numpy(emb_norm_np).to(self.device, dtype=torch.float32)
                for mlp_model, key_name in self.mlp_configs:
                    out = mlp_model(emb_norm_tensor)
                    mlp_results[key_name] = tensor_to_float(out)

                results[path] = {
                    "clip_scores": clip_scores_dict,
                    **mlp_results,
                }
        return results

    # -----------------------------
    # Main function: infer_many
    # -----------------------------
    def infer_many(self, image_paths: List[str]) -> pd.DataFrame:
        """Overridden pipeline:
        1) Temporarily set TOKENIZERS_PARALLELISM="false".
        2) Load any cached embeddings from h5.
        3) Compute embeddings for new images.
        4) Compute final scores (CLIP + MLP).
        5) Return a DataFrame with columns:
           [filename, clip_scores, <mlp_keys>... ]
           where 'filename' is the *original* path.
        """
        old_env = os.environ.get("TOKENIZERS_PARALLELISM", None)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

        try:
            # 1) Identify missing embeddings
            to_process = self._load_cached_embeddings(image_paths)

            # 2) Compute embeddings for missing images
            self._compute_embeddings_for(to_process)

            # 3) Compute final scores from all embeddings
            results_dict = self._compute_scores_from_features()

        finally:
            # restore environment variable
            if old_env is None:
                del os.environ["TOKENIZERS_PARALLELISM"]
            else:
                os.environ["TOKENIZERS_PARALLELISM"] = old_env

        # 4) Convert results_dict => DataFrame
        rows = []
        for path, score_dict in results_dict.items():
            # We'll store the normal path in 'filename'
            row = {"filename": path, "clip_scores": score_dict["clip_scores"]}
            for k, v in score_dict.items():
                if k == "clip_scores":
                    continue
                row[k] = v
            rows.append(row)

        return pd.DataFrame(rows)
