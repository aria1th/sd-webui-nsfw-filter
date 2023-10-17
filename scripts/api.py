"""
Registers API routes for the webui
"""
import gradio as gr
import base64
import io
from secrets import compare_digest
from fastapi import HTTPException
from fastapi import Depends, FastAPI, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
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
    api_credentials = {}
    dependencies = None
    from modules import shared
    
    def auth(credentials:HTTPBasicCredentials = Depends(HTTPBasic())):
        if credentials.username in api_credentials and compare_digest(credentials.password, api_credentials[credentials.username]):
            return True
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    if shared.cmd_opts.api_auth:
        api_credentials = {}
        for cred in shared.cmd_opts.api_auth.split(","):
            if ":" not in cred or cred.count(":") > 1:
                # skip invalid credentials
                continue
            user, password = cred.split(":")
            if user in api_credentials:
                # skip duplicate users
                continue
            api_credentials[user] = password
        dependencies = [Depends(auth)]
    @app.post("/safety/predict", response_model=SafetyResponse, dependencies=dependencies)
    def check_safety(image:str = Form(...)):
        """
        Check if image is NSFW.
        curl -X POST "http://localhost:7860/safety/predict" -H  "accept: application/json" -H  "Content-Type: application/x-www-form-urlencoded" -d "image=base64encodedimage"
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
