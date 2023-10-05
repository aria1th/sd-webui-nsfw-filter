import launch
import torch.cuda as cuda
# launch is imported in context of webui
if not launch.is_installed("onnxruntime") and not launch.is_installed("onnxruntime-gpu"):
    print("Installing onnxruntime")
    launch.install("onnxruntime-gpu" if cuda.is_available() else "onnxruntime")

