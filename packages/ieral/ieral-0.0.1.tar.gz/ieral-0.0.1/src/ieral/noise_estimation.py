import numpy as np

def median_absolute_deviation(signal: np.ndarray) -> float:
    """
    Estimate the noise level of a signal using the median absolute deviation
    method.
    Args:
        signal: The signal to estimate the noise level of
    Returns:
        The estimated noise level
    """
    return np.median(np.abs(signal - np.median(signal))) / 0.6745

def variance_of_diff(signal: np.ndarray) -> float:
    """ Estimate the noise level of a signal using the variance of the diff. signal.
    
    Args:
        signal: The signal to estimate the noise level of
    Returns:
        The estimated noise level
    """
    signal_diff = np.diff(signal)
    signal_diff_std = np.std(signal_diff)
    return signal_diff_std/np.sqrt(2)
