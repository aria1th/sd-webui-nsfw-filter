from modules.script_callbacks import on_before_image_saved, ImageSaveParams
from scripts.predict import is_nsfw
import modules.scripts as scripts
import torch
import numpy as np
from PIL import Image, ImageFilter

def censor_nsfw(image: Image.Image) -> Image.Image:
    if is_nsfw(image):
        image = image.filter(ImageFilter.GaussianBlur(20))
    return image

def on_callback(params: ImageSaveParams):
    params.image = censor_nsfw(params.image)
    
    
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