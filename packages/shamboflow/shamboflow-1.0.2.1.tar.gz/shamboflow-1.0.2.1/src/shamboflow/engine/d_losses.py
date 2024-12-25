"""Partial derivatives of loss functions"""

import numpy as np
import cupy as cp

from shamboflow import IS_CUDA

def d_MSE(pred_val : np.ndarray, obs_val : np.ndarray) -> np.ndarray :
    """Derivative of Mean Squared Error loss function
    
    ``Formula : y_pbserved - y_predicted``
    """

    if IS_CUDA :
        pred_val = cp.asarray(pred_val)
        obs_val = cp.asarray(obs_val)
        res = cp.subtract(obs_val, pred_val)
        return cp.asnumpy(res)
    
    return np.subtract(obs_val, pred_val)

def get(func : str) :
    """Helper function to get a loss function derivative

    Return the appropriate loss function derivative
    depending on the given string

    Args
        func:
            Query string for the requested loss function derivative

    Returns
        Appropriate function
    """

    func = func.strip().lower()

    if func == "mean_squared_error" :
        return d_MSE