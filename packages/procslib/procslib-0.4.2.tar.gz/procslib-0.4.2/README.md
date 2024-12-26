# procslib

[![ci](https://github.com/arot-devs/procslib/workflows/ci/badge.svg)](https://github.com/arot-devs/procslib/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://arot-devs.github.io/procslib/)
[![pypi version](https://img.shields.io/pypi/v/procslib.svg)](https://pypi.org/project/procslib/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#procslib:gitter.im)

**Multi-purpose processing library** for various inference tasks.  
Generated with [copier-uv](https://github.com/pawamoy/copier-uv).

---

## Installation

```bash
pip install procslib
```

Or using [`uv`](https://docs.astral.sh/uv/):

```bash
uv tool install procslib
```

## Quick Usage

Below is a minimal example of how to infer images with `procslib`:

```python
from procslib import get_model_keys, get_model

# List available models
print(get_model_keys())

# Create a model, e.g. "twitter_logfav"
model = get_model("twitter_logfav")

# Infer on some images
image_paths = ["path/to/image1.jpg", "path/to/image2.jpg"]
results_df = model.infer_many(image_paths)
print(results_df.head())
```

## Supported Models

You can retrieve a model via `get_model(key)`. Here’s a quick reference:

| Key                    | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| `twitter_logfav`       | A model predicting Twitter favorites (log-scaled) for anime images |
| `weakm_v2`             | A previous version of numeric aesthetics scoring (anime)     |
| `siglip_aesthetic`     | A Siglip-based aesthetic model for general images (requires a newer transformers) |
| `pixiv_compound_score` | A numeric aesthetics score model trained on pixiv data       |
| `cv2_metrics`          | Basic image metrics (noise, exposure, clarity, edge count, etc.) (No GPU usage) |
| `complexity_ic9600`    | A complexity-measuring model for images                      |
| `rtmpose`              | Detects body parts in images (RTMDet-based)                  |
| `depth`                | MiDaS-based depth estimation (returns a “depthness” metric)  |
| `q_align_quality`      | Q-Align model for quality assessment (requires `transformers==4.36.1`) |
| `q_align_aesthetics`   | Q-Align model for aesthetics (also needs that older `transformers`) |
| `laion_watermark`      | A fast watermark (text detection) model from LAION           |
| `clip_aesthetic`       | Caches CLIP embeddings and calculates aesthetic scores and 0-shot classifications from embeddings|

> **Note**: Q-Align and Siglip Aesthetics are incompatible with each other’s `transformers` version.
> If you need both, see [Docs: Handling Conflicting Dependencies]().

## Development

For development tasks (testing, formatting, releasing), see [Dev Guide]() or run:

```bash
make setup   # one-time
make format  # auto-format
make test
make check
make changelog
make release version=x.y.z
```

## Documentation

To learn more, visit our [MkDocs-based docs](https://arot-devs.github.io/procslib/) or run:

```bash
make docs host=0.0.0.0
```

- [Quick Start: Using Models]()
- [Quick Start: Adding New Models]()
- [VSCode Tips]()