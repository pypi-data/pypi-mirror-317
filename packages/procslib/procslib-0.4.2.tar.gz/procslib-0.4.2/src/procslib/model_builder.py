import hashlib
import os

# ===== ADD YOUR MODELS BELOW =====


def get_twitter_logfav_model():
    """A model trained for predicting Twitter log-favorites using AnimeAestheticInference.
    输入anime图片, 输出预测的推特点赞数量(lognp'ed)
    """
    from procslib.models import AnimeAestheticInference

    checkpoint_path = "/rmt/yada/dev/training-flow/models/convbase_twitter_aes_logfav_full_v2cont3_e4_mae0.50.ckpt"
    return AnimeAestheticInference(checkpoint_path=checkpoint_path, column_name="twitter_logfav_score")


def get_weakm_v2_model():
    """A model trained for WeakM aesthetic predictions (v2) with low mean absolute error.
    输入anime图片, 输出预测的weakm v2 score (base score:10)
    """
    from procslib.models import AnimeAestheticInference

    checkpoint_path = "/rmd/yada/checkpoints/aesthetics_weakm-v2_volcanic-salad-49/epoch=4,mae=0.0824,step=0.ckpt"
    return AnimeAestheticInference(checkpoint_path=checkpoint_path, column_name="weakm_v2_score")


def get_siglip_aesthetic_model():
    """A Siglip-based aesthetic model for high-efficiency aesthetic predictions.
    输入anime图片, 输出预测的siglip aesthetic score
        https://github.com/discus0434/aesthetic-predictor-v2-5
    """
    from procslib.models import SiglipAestheticInference

    return SiglipAestheticInference(device="cuda", batch_size=32)


def get_pixiv_compound_score_model():
    """Aesthetic model trained on pixiv data (of the constructed pixiv compound aesthetic score)
    model at "https://bucket-public-access-uw2.s3.us-west-2.amazonaws.com/dist/compound_score_aesthetic_predictor/model.ckpt"
    """
    from procslib.models import PixivCompoundScoreInference

    checkpoint_path = "/rmd/yada/checkpoints/pixiv_compound_aesthetic_convtiny_larry.ckpt"
    return PixivCompoundScoreInference(model_path=checkpoint_path, column_name="pixiv_compound_score")


def get_complexity_ic9600_model():
    """A model trained for predicting image complexity using the IC9600 model.
    输入图片, 输出图片复杂度评分
    """
    from procslib.models import IC9600Inference

    model_path = "/rmd/yada/model_weights/complexity_ic9600_ck.pth"
    return IC9600Inference(model_path=model_path, device="cuda", batch_size=32)


def get_cv2_metrics_model():
    """Calculates OpenCV-based image metrics such as brightness, contrast, noise level, etc.
    输入图片, 输出图片质量评分
    """
    from procslib.models import OpenCVMetricsInference

    return OpenCVMetricsInference(device="cpu", batch_size=32)


def get_rtmpose_model():
    """A model trained for human pose estimation using RTMPose.
    输入图片, 输出人体姿势关键点
    """
    from procslib.models import RTMPoseInference

    onnx_file = "/rmd/yada/checkpoints/rtmpose-l_8xb256-420e_humanart-256x192-389f2cb0_20230611_e2e.onnx"
    return RTMPoseInference(onnx_file=onnx_file, device="cuda")


def get_depth_model(**overrides):
    """Using "Intel/dpt-hybrid-midas" model for depth estimation and exports a 'depthness' score.
    输入图片, 输出图片深度分 (0.0-1.0, higher is more depth)
    """
    from procslib.models.depth_wrapper import DepthEstimationInference

    return DepthEstimationInference(
        **overrides,
    )


def get_q_align_quality_model(**overrides):
    """A model trained for predicting image quality using QAlign.
    输入图片, 输出图片质量评分
    """
    from procslib.models.q_align import QAlignAsyncInference

    return QAlignAsyncInference(task="quality", **overrides)


def get_q_align_aesthetics_model(**overrides):
    """A model trained for predicting image aesthetics using QAlign.
    输入图片, 输出图片美学评分
    """
    from procslib.models.q_align import QAlignAsyncInference

    return QAlignAsyncInference(task="aesthetics", **overrides)


def get_laion_watermark_model(**overrides):
    """A model trained for predicting watermarks using Laion.
    输入图片, 输出水印评分
    """
    from procslib.models.laion_watermark import LaionWatermarkInference

    return LaionWatermarkInference(**overrides)


def get_cached_clip_aesthetic_model(batch_size=32, **overrides):
    import unibox as ub

    from procslib.models.clip_aesthetic_cached import CachedClipAestheticInference, get_mlp_model
    from procslib.utils.utils import get_gpu_id_from_env

    # Default configurations
    clip_prompts = ub.loads("s3://bucket-external/misc/yada_store/configs/clip_prompts_list_full_v2.txt")
    clip_mlp = get_mlp_model("kiriyamaX/clip-aesthetic")
    twitter_mlp = get_mlp_model("kiriyamaX/twitter-aesthetic-e20")
    twitter_v2_mlp = get_mlp_model("kiriyamaX/twitter-aesthetic-v2-e10")

    mlp_configs = [
        (clip_mlp, "clip_aesthetic"),
        (twitter_mlp, "twitter_aesthetic"),
        (twitter_v2_mlp, "twitter_aesthetic_v2"),
    ]

    device_id = get_gpu_id_from_env()
    random_hash = hashlib.sha1(os.urandom(8)).hexdigest()[:4]
    h5_path = f"./clip_cache_gpu{device_id}_{random_hash}.h5"

    config = {
        "prompts_list": clip_prompts,
        "mlp_configs": mlp_configs,
        "h5_path": h5_path,
        "device": "cuda",
        "batch_size": batch_size,
        "num_workers": 8,
    }
    config.update(overrides)
    return CachedClipAestheticInference(**config)


MODEL_REGISTRY = {
    "twitter_logfav": get_twitter_logfav_model,
    "weakm_v2": get_weakm_v2_model,
    "siglip_aesthetic": get_siglip_aesthetic_model,
    "pixiv_compound_score": get_pixiv_compound_score_model,
    "cv2_metrics": get_cv2_metrics_model,
    "complexity_ic9600": get_complexity_ic9600_model,
    "rtmpose": get_rtmpose_model,
    "depth": get_depth_model,
    "q_align_quality": get_q_align_quality_model,
    "q_align_aesthetics": get_q_align_aesthetics_model,
    "laion_watermark": get_laion_watermark_model,
    "clip_aesthetic": get_cached_clip_aesthetic_model,
}


# ============ DO NOT EDIT BELOW THIS LINE ============


def get_model_keys():
    """Retrieves the keys and descriptions of the model registry.

    Returns:
        dict: A dictionary where keys are model names and values are descriptions.
    """
    return {key: func.__doc__.strip() for key, func in MODEL_REGISTRY.items()}


def get_model(descriptor: str, **overrides):
    """Retrieves the actual model instance associated with the given descriptor.

    Args:
        descriptor (str): The model descriptor key in the MODEL_REGISTRY.

    Returns:
        object: The model instance.

    Raises:
        ValueError: If the descriptor is not found in MODEL_REGISTRY.
    """
    if descriptor not in MODEL_REGISTRY:
        raise ValueError(f"Descriptor '{descriptor}' not found in MODEL_REGISTRY.")
    return MODEL_REGISTRY[descriptor](**overrides)
