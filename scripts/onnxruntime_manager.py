from onnxruntime import InferenceSession, SessionOptions, GraphOptimizationLevel
def open_onnx_model(ckpt: str, use_cuda: bool=True) -> InferenceSession:
    """
    Open ONNX model and returns session
    
    @param ckpt: path to checkpoint
    """
    options = SessionOptions()
    options.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_ALL
    return InferenceSession(ckpt, options, providers=
                            ['CUDAExecutionProvider' if use_cuda else 'CPUExecutionProvider']
                        ) # session
    
    