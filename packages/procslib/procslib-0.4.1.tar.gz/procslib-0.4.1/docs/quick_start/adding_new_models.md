# Adding and testing new model

## Adding a new model

要添加一个新的模型到procslib, 首先在`./models`文件夹下创建一个新文件, 继承`BaseImageInference`类:

- 然后实现`__init__`, `load_model`, `preprocess`, `postprocess`, `infer`方法等`BaseImageInference`类要求的method

- (如果已经有可用的模型推理代码, 可以直接用gpt来很快生成inference class的对应代码)


```python
# src/procslib/models/cv2_wrapper.py
class OpenCVMetricsInference(BaseImageInference):
    """A class to calculate simple image metrics (brightness, contrast, etc.)
    using OpenCV or NumPy.
    """

    def __init__(self, device="cpu", batch_size=32):
        # device is mostly irrelevant here since no GPU ops
        super().__init__(device=device, batch_size=batch_size)

    def _load_model(self, checkpoint_path: str = None):
        # No model to load
        pass

    # ... implements all the necessary methods defined at the base class:
    # src/procslib/models/base_inference.py


```

<br>

然后在`./models/__init__.py`中导入新的inference class:

```python
# src/procslib/models/__init__.py
from .cv2_wrapper import OpenCVMetricsInference
```

<br>

然后在`./model_builder.py`里写一个新的model builder method, 返回新定义模型的inference instance:

```python
# src/procslib/model_builder.py
def get_cv2_model():
    """
    (add your model descriptions as docstring)
    """
    from procslib.models import OpenCVMetricsInference
    
    return OpenCVMetricsInference()
```

<br>

然后在(`model_builder.py`)下面一点的位置, 添加刚写的builder method到`MODEL_REGISTRY`变量:

```python
# src/procslib/model_builder.py
MODEL_REGISTRY = {
    # existing model definitions
    "twitter_logfav": get_twitter_logfav_model,
    "weakm_v2": get_weakm_v2_model,
    "siglip_aesthetic": get_siglip_aesthetic_model,
    "pixiv_compound_score": get_pixiv_compound_score_model,

    # add your model here
    "cv2_metrics": get_cv2_model,
}
```

这样就可以在其他地方通过`get_model("cv2_metrics")`来获取新的模型了.

## Testing the new model

可以在notebook里检查新添加的模型是否正常工作:

<br>

查看可用的模型:
```python
from procslib import get_model_keys, get_model

# get available models; this should print a dict of available model keys and their docstring descriptions
get_model_keys() 

# {'twitter_logfav': "A model trained for predicting Twitter log-favorites using AnimeAestheticInference.\n    输入anime图片, 输出预测的推特点赞数量(lognp'ed)",
#  'weakm_v2': 'A model trained for WeakM aesthetic predictions (v2) with low mean absolute error.\n    输入anime图片, 输出预测的weakm v2 score (base score:10)',
#  'siglip_aesthetic': 'A Siglip-based aesthetic model for high-efficiency aesthetic predictions.\n    输入anime图片, 输出预测的siglip aesthetic score\n        https://github.com/discus0434/aesthetic-predictor-v2-5',
#  'pixiv_compound_score': 'aesthetic model trained on pixiv data (of the constructed pixiv compound aesthetic score)\n    model at "https://bucket-public-access-uw2.s3.us-west-2.amazonaws.com/dist/compound_score_aesthetic_predictor/model.ckpt"'}
```

<br>

使用模型:
```python
from procslib import get_model_keys, get_model

key = "cv2_metrics"
model = get_model(key)
image_path = "path/to/image.jpg"
iamge_paths_list = ["path/to/image1.jpg", "path/to/image2.jpg"]

# one image
res1 = model.infer_one(image_path)

# batch of images (one batch)
res2 = model.infer_batch(image_paths_list)

# many images using dataloader (batched)
res3 = model.infer_many(image_paths_list)
```

<br>

如果要在一些图片上批量计算metrics, 可以直接输入不同的model key:
```python

import unibox as ub
from procslib import get_model_keys, get_model

# local download folder, contain images or folders of images
DST_FOLDER = "/lv0/yada/aesthetic_eagle_5category_iter99_images"

# local metrics folder
DATA_SAVE_DIR = "../data".strip("/")
img_paths = ub.traverses(DST_FOLDER, ub.IMG_FILES)

# get available commands
# get_model_keys()

TODO_KEYS = [
    "twitter_logfav",
    "weakm_v2",
    "siglip_aesthetic",
    "pixiv_compound_score",
]

res = {}
for key in TODO_KEYS:
    print(f"getting {key} model...")
    model = get_model(key)

    print(f"Processing {key}...")
    _res = model.infer_many(img_paths)

    print(f"Done processing {key} | {len(_res)}")
    res[key] = _res

for key, val in res.items():
    ub.saves(val, f"{DATA_SAVE_DIR}/eagle_5cat_metrics_{key}.parquet")
```
