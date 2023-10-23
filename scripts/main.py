from modules.script_callbacks import on_before_image_saved, ImageSaveParams
from scripts.predict import is_nsfw
import modules.scripts as scripts
import torch
import numpy as np
from PIL import Image, ImageFilter
from modules import shared


def censor_nsfw(image: Image.Image) -> Image.Image:
    if is_nsfw(image):
        image = image.filter(ImageFilter.GaussianBlur(20))
    return image


def on_callback(params: ImageSaveParams):
    params.image = censor_nsfw(params.image)


def close_wrapper(fun):
    def wrapper(*args, **kwargs):
        try:
            original_assign_current_image = getattr(shared.state, 'original_assign_current_image', None)
            if original_assign_current_image:
                shared.state.assign_current_image = original_assign_current_image
                shared.state.original_assign_current_image = None
        except Exception as e:
            print(e)
        return fun(*args, **kwargs)
    return wrapper


class Script(scripts.Script):
    
    def __init__(self):
        pass
    
    def title(self):
        return "NSFW Filter"
    
    def show(self, is_img2img):
        return scripts.AlwaysVisible 
    
    def postprocess_image(self, p, pp, *args):
        pp.image = censor_nsfw(pp.image)


on_before_image_saved(on_callback)
print("NSFW filter installed, this will be applied to all images saved from now on")


def assign_current_image_wrapper(original_function):
    def wrapper_function(*args, **kwargs):
        try:
            return original_function(censor_nsfw(args[0]), *args[1:], **kwargs)
        except Exception as e:
            print(e)
        return original_function(*args, **kwargs)
    return wrapper_function


if getattr(shared.state, 'original_assign_current_image_nsfw_filter', None) is None:
    shared.state.original_assign_current_image_nsfw_filter = shared.state.assign_current_image
    shared.state.assign_current_image = assign_current_image_wrapper(shared.state.assign_current_image)
