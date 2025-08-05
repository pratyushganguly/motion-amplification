"""
General utilities (chunking, backend checks, etc.)
"""
import cv2

def choose_backend(req):
    """
    Choose the best available backend for processing.
    
    Args:
        req: Requested backend ("auto", "cpu", "cuda", "opencl")
        
    Returns:
        str: Selected backend name
    """
    if req == "cpu": 
        return "cpu"
    if req == "cuda": 
        return "cuda" if cv2.cuda.getCudaEnabledDeviceCount() > 0 else "cpu"
    if req == "opencl": 
        return "opencl" if cv2.ocl.haveOpenCL() else "cpu"
    
    # Auto selection
    if cv2.cuda.getCudaEnabledDeviceCount() > 0: 
        return "cuda"
    if cv2.ocl.haveOpenCL(): 
        return "opencl"
    return "cpu"