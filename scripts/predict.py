from PIL import Image
from functools import lru_cache
from huggingface_hub import hf_hub_download
from scripts.onnxruntime_manager import open_onnx_model
import numpy as np
import torch


FILTER_MODEL = None

def load_filter_model():
    global FILTER_MODEL
    if FILTER_MODEL is None:
        FILTER_MODEL = _load_model()
    return FILTER_MODEL

@lru_cache(maxsize=1)
def _load_model():
    return open_onnx_model(
        hf_hub_download(
            'deepghs/imgutils-models', # thank you deepghs for converting to onnx
            'nsfw/nsfwjs.onnx'
        ),
        torch.cuda.is_available()
    )

def is_nsfw(image: Image) -> bool:
    """
    Determine if image is NSFW
    Includes 'hentai', 'porn', 'sexy' as NSFW labels.
    WARN : The model has bias, it may not be able to detect certain types of NSFW images.
    """
    model = load_filter_model() # session 
    image = image.convert('RGB').resize((224, 224), Image.NEAREST)
    # as ndarray
    image = ((np.array(image) / 255.0)[None,...]).astype(np.float32)
    scores, = model.run(['dense_3'], {'input_1': image})
    max_idx = np.argmax(scores)
    # _labels = ['drawings', 'hentai', 'neutral', 'porn', 'sexy'] # from nsfwjs repo
    # strict
    if max_idx in [1, 3, 4]:
        return True
    return False
    