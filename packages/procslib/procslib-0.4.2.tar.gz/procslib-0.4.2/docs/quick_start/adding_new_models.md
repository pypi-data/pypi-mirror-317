# Adding and Testing New Models

This page describes how to extend `procslib` with additional models.

## 1. Create a new inference class

In `src/procslib/models`, create a file for your new model. Inherit from `BaseImageInference`:

```python
from .base_inference import BaseImageInference

class MyNewModelInference(BaseImageInference):
    def __init__(self, device="cuda", batch_size=32):
        super().__init__(device=device, batch_size=batch_size)
        self._load_model()

    def _load_model(self, checkpoint_path=None):
        # load your model

    def _preprocess_image(self, pil_image):
        # preprocess

    def _postprocess_output(self, logits):
        # interpret

    # Optionally override infer_many if you have custom logic
```

## 2. Register the new model

In `src/procslib/model_builder.py`, add a builder function:

```python
def get_my_new_model():
    """
    My new model for fancy tasks
    """
    from procslib.models.my_new_model import MyNewModelInference
    return MyNewModelInference()
```

Then add it to `MODEL_REGISTRY`:

```python
MODEL_REGISTRY["my_new_model"] = get_my_new_model
```

Now you can call:

```python
model = get_model("my_new_model")
model.infer_many(["img1.jpg", "img2.jpg"])
```

## 3. Test in a notebook

```python
from procslib import get_model
model = get_model("my_new_model")
df = model.infer_many(["/some/path.jpg"])
print(df)
```

That’s it!
