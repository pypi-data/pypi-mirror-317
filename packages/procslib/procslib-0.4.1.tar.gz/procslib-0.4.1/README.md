# procslib

[![ci](https://github.com/arot-devs/procslib/workflows/ci/badge.svg)](https://github.com/arot-devs/procslib/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://arot-devs.github.io/procslib/)
[![pypi version](https://img.shields.io/pypi/v/procslib.svg)](https://pypi.org/project/procslib/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#procslib:gitter.im)

Multi-purpose processing library for downstream use. Project generated with [copier-uv](https://github.com/pawamoy/copier-uv)

## Installation

```bash
pip install procslib
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv tool install procslib
```



## Usage

procslib allows inference with many models using a single interface, by sumbitting different keys, similar to Huggingface AutoModels:

```python
from procslib import get_model_keys, get_model

# get available keys
print(get_model_keys())

# create a model
model = get_model("twitter_logfav")

# do inference
iamge_paths_list = ["path/to/image1.jpg", "path/to/image2.jpg"]
res_df = model.infer_many(image_paths_list)
```

### Supported Models:

the models can be retrieved by calling `get_model(key)` where `key` is one of the following:

- note that Q-Align models requires `transformers==4.36.1`, which is incompatible with `siglip_aesthetic`.


| key                    | field   | description                                                  | backbone           |
| ---------------------- | ------- | ------------------------------------------------------------ | ------------------ |
| `twitter_logfav`       | anime   | log(predicted twitter favorite count)                        | convnext v2 base   |
| `weakm_v2`             | anime   | previous version of numerical aesthetics score               | convnext v2 base   |
| `siglip_aesthetic`     | general | an Clip Aesthetics alternative that uses siglip backbone and with better performance on anime<br />[discus0434/aesthetic-predictor-v2-5](https://github.com/discus0434/aesthetic-predictor-v2-5) | siglip (vit) + mlp |
| `pixiv_compound_score` | anime   | numerical aesthetics score based on pixiv bookmarks and other metrics | convnext v2 tiny   |
| `cv2_metrics`          | general | many useful image related metrics, such as noise, exposure, edge count, etc | (Not a model)      |
| `complexity_ic9600`    | general | a model that analyzes the "complexity" of images<br />[tinglyfeng/IC9600](https://github.com/tinglyfeng/IC9600) | ICNet (resnet18)   |
| `rtmpose`              | general | analyzes the presence of body parts of images<br />[mmpose/projects/rtmpose at main](https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose) | RTMDet             |
| `depth`                | general | using MiDaS 3.0 to analyze the "depthness" of images and returns a numerical metric<br />[Intel/dpt-hybrid-midas · Hugging Face](https://huggingface.co/Intel/dpt-hybrid-midas) | MiDaS              |
| `q_align_quality`      | general | image quality assessment using Q-Align model (rough/distorted images = lower score; refined images = higher score)<br />[Q-Future/Q-Align](https://github.com/Q-Future/Q-Align) | VLM                |
| `q_align_aesthetics`   | general | image aesthetics assessment using Q-Align model (warn: has a western, or "midjourney-like" taste for higher qualities)<br />[Q-Future/Q-Align](https://github.com/Q-Future/Q-Align) | VLM                |
| `laion_watermark`      | general | a very fast watermark detection model that detects if there's text on the image. (works 80% of the time but could be inaccurate)<br />[LAION-AI/LAION-5B-WatermarkDetection](https://github.com/LAION-AI/LAION-5B-WatermarkDetection) | EfficientNet B3    |
| `clip_aesthetic`       | general | (WIP) caches clip embeddings, calculates similarities with a given list of prompts, then outputs aesthetics scores by supplying a list of MLP models. Very fast when embeddings are cached.<br />[troph-team/pixai-aesthetic](https://github.com/troph-team/pixai-aesthetic/tree/main) | clip (vit) + mlp   |





## Development


for how to navigate the project repo (generate changelogs, release versions, etc) see the [project template documentation](https://pawamoy.github.io/copier-uv/work/):

```bash
make setup  # only once

<write code>
make format  # to auto-format the code

<write tests>
make test  # to run the test suite

make check  # to check if everything is OK

<commit your changes>

make changelog  # to update the changelog
<edit changelog if needed>

make release version=x.y.z  # to release a new version (find the exact version number to use from CHANGELOG.md)
```

## Documentation

To view (and live edit) the documentations, run:

```bash
make docs host=0.0.0.0
```