"""
Temporal filtering and amplification functions.
"""
from scipy import signal

def apply_temporal_filter(luma_stack, sos, alpha):
    """
    Applies a bandpass filter along the time axis, then amplifies.
    
    Args:
        luma_stack: 3D array (time, height, width) of luma values
        sos: Filter coefficients from scipy.signal.butter
        alpha: Amplification factor
        
    Returns:
        np.ndarray: Amplified luma stack
    """
    filtered = signal.sosfiltfilt(sos, luma_stack, axis=0)
    return luma_stack + alpha * filtered