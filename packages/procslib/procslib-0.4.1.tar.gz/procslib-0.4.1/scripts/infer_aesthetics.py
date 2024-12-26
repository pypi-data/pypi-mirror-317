import argparse
import os

import pandas as pd
import unibox as ub

from procslib.models.anime_aesthetic_cls import AnimeAestheticClassificationInference

# load model
CHECKPOINT_PATH = "/rmd/yada/checkpoints/aesthetics_cls_6k-mix_soft-firebrand-34/e9_acc0.8120.ckpt"
PATH_COLUMN = "local_path"
SAVE_DIR = ""  # save to the same directory as the input file


def main(checkpoint_path, path_column, save_dir, paths_file, batch_size=64):
    model = AnimeAestheticClassificationInference(
        checkpoint_path=checkpoint_path,
        num_classes=5,
    )

    # load data
    df = pd.read_parquet(paths_file)
    img_paths = df[path_column].tolist()
    print("Data file loaded:", ub.peeks(img_paths))

    # infer
    res = model.infer_many(img_paths, batch_size=batch_size)
    print("Inference done:", ub.peeks(res))

    # save results
    orig_filename = os.path.basename(paths_file)  # *.parquet
    save_filename = f"{orig_filename}_tagged.parquet"
    save_path = os.path.join(save_dir, save_filename)
    os.makedirs(save_dir, exist_ok=True)
    ub.saves(res, save_path)


def parse_args():
    parser = argparse.ArgumentParser(description="Infer aesthetics")
    parser.add_argument("--paths_file", type=str, required=True)
    parser.add_argument("--checkpoint_path", type=str, default=CHECKPOINT_PATH)
    parser.add_argument("--path_column", type=str, default=PATH_COLUMN)
    parser.add_argument("--save_dir", type=str, default=SAVE_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    # python /lv0/test_aesthetics/procslib/scripts/infer_aesthetics.py --paths_file 0.parquet

    # bs32: 15744MiB / 81559MiB
    # bs64: 27484MiB / 81559MiB
    args = parse_args()
    main(args.checkpoint_path, args.path_column, args.save_dir, args.paths_file)
