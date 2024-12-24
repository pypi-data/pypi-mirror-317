"""A Collection of derivatives for the activation functions"""

import numpy as np
import cupy as cp

from shamboflow import IS_CUDA
from shamboflow.engine import activations

def d_sigmoid(x : np.ndarray, **kwargs) -> np.ndarray :
    """The partial derivative of sigmoid function
    
    If sigmoid is g(x)
    ``g'(x) = g(x)(1 - g(x))`` 
    """

    if IS_CUDA :
        res_sig = cp.asarray(activations.sigmoid(x))
        res_d_sig = cp.multiply(res_sig, cp.subtract(1, res_sig))
        return cp.asnumpy(res_d_sig)
    
    res_sig = activations.sigmoid(x)
    res_d_sig = np.multiply(res_sig, np.subtract(1, res_sig))
    return res_d_sig

def d_tanh(x : np.ndarray, **kwargs) -> np.ndarray :
    """The partial derivative for hyperbolic tangent
    
    If tanh is g(x)
    ``g'(x) = 1 - g(x)^2``
    
    """

    if IS_CUDA :
        res_tanh = cp.asarray(activations.tanh(x))
        res_d_tanh = cp.subtract(1, cp.power(res_tanh, 2))
        return cp.asnumpy(res_d_tanh)
    
    res_tanh = activations.tanh(x)
    res_d_tanh = np.subtract(1, np.power(res_tanh, 2))
    return res_d_tanh

def d_relu(x : np.ndarray, **kwargs) -> np.ndarray :
    """Partial derivative for relu function

    ``Formula: 0 if x < 0 else 1``
    
    """

    if IS_CUDA :
        x_gpu = cp.asarray(x)
        res = cp.where(x_gpu < 0, 0, 1)
        return cp.asnumpy(res)
    
    return np.where(x < 0, 0, 1)

def d_leakyrelu(x : np.ndarray, leakyrelu_slope : float, **kwargs) -> np.ndarray :
    """Partial derivative for leaky relu function
    
    ``Formula: slope if x < 0 else 1``
    """

    if IS_CUDA :
        x_gpu = cp.asarray(x)
        res = np.where(x_gpu < 0, leakyrelu_slope, 1)
        return cp.asnumpy(res)
    
    return np.where(x < 0, leakyrelu_slope, 1)

def d_softmax(x : np.ndarray, **kwargs) -> np.ndarray :
    """Not implemented yet"""
    pass


def get(func : str) :
    """Helper function to get an activation function derivative

    Return the appropriate activation function
    depending on the given string

    Args
        func:
            Query string for the requested activation function derivative

    Returns
        Appropriate function
    """
    # TODO : handle wrong inputs
    if not isinstance(func, str) :
        ...

    func = func.strip().lower()

    if func == "sigmoid" :
        return d_sigmoid
    elif func == "tanh" :
        return d_tanh
    elif func == "relu" :
        return d_relu
    elif func == "leakyrelu" :
        return d_leakyrelu
    # elif func == "softmax" :
    #     return softmax