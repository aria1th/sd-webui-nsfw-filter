import launch
# launch is imported in context of webui
if not launch.is_installed("onnxruntime") and not launch.is_installed("onnxruntime-gpu"):
    import torch.cuda as cuda
    print("Installing onnxruntime")
    launch.run_pip("install onnxruntime-gpu" if cuda.is_available() else "install onnxruntime")
