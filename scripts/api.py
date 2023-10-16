"""
Registers API routes for the webui
"""
import gradio as gr
import base64
import io
from fastapi import FastAPI, Form
from pydantic import BaseModel


from scripts.predict import is_nsfw

class SafetyResponse(BaseModel):
    """
    Safety response.
    """
    is_nsfw: bool
    
def register_safety_api(app:FastAPI):
    """
    Registers safety API routes.
    """
    @app.post("/safety/predict", response_model=SafetyResponse)
    def check_safety(image:str = Form(...)):
        """
        Check if image is NSFW.
        """
        # Image.open(io.BytesIO(base64.b64decode(i)))
        image = io.BytesIO(base64.b64decode(image))
        return SafetyResponse(is_nsfw=is_nsfw(image))

def register_api(_:gr.Blocks, app:FastAPI):
    """
    Registers hooks for app on webui startup
    """
    register_safety_api(app)

# only works in context of sdwebui
try:
    import modules.script_callbacks as script_callbacks
    script_callbacks.on_app_started(register_api)
except (ImportError, ModuleNotFoundError) as e:
    print("Could not bind safety-checker api routes")
