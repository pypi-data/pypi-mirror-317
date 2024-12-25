"""Common Activation functions"""

import numpy as np
import cupy as cp
from shamboflow import IS_CUDA

def sigmoid(x : np.ndarray, **kwargs) -> np.ndarray :
    """Sigmoid acitvation function
    
    Applies the sigmoid activation function to a value.
    It returns a value between 0 and 1 but never 0 and 1.
    It suffers from the vanishing gradient issue.

    ``sigmoid(x) = 1 / (1 + exp(-x))``

    Range: (0, 1)

    Args
        x:
            The input vector to apply activation function over.

    Returns
        Value after sigmoid is applied on x
    
    """

    if IS_CUDA :
        try :
            x_gpu = cp.asarray(x)
            res = (1 / (1 + cp.exp(-x_gpu)))
            return cp.asnumpy(res)
        except :
            pass

    return (1 / (1 + np.exp(-x)))

def tanh(x : np.ndarray, **kwargs) -> np.ndarray :
    """Hyperbolic tangent activation function

    ``tanh(x) = (exp(x) - exp(-x)) / (exp(x) + exp(-x))``

    Range: (-1, 1)

    Args
        x:
            The input vector to apply activation function over.

    Returns
        Value after tanh is applied on x
    
    """

    if IS_CUDA :
        try :
            x_gpu = cp.asarray(x)
            res = (cp.exp(x_gpu) - cp.exp(-x_gpu)) / (cp.exp(x_gpu) + cp.exp(-x_gpu))
            return cp.asnumpy(res)
        except :
            pass
    
    return ((np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x)))

def relu(x : np.ndarray, **kwargs) -> np.ndarray :
    """ReLU activation function
    
    Applies the ReLU activation function on the input x.

    ReLU or Rectilinear Unit was devised to overcome
    the issue of vanishing gradient in sigmoid function. It resolves
    the issue by not having any upper limit. But that comes with
    its own problems.

    ``ReLU(x) = max(0, x)``

    Range: [0, inf)

    Args
        x:
            The input vector to apply activation function over.

    Returns
        Value after relu is applied on x
    """

    if IS_CUDA :
        try :
            x_gpu = cp.asarray(x)
            res = cp.fmax(0, x_gpu)
            return cp.asnumpy(res)
        except :
            pass

    return np.fmax(0, x)

def leakyrelu(x : np.ndarray, leakyrelu_slope : float, **kwargs) -> np.ndarray :
    """Leaky ReLU activation function
    
    This function was devised to address
    the issue of negative values as input
    to ReLU. ReLU would simply discard
    them, but leaky relu uses them as well.

    ``leakyReLU(x, slope) = if (x > 0) => x, if (x <= 0) => slope * x``

    Range: (-inf, inf)

    Args
        x:
            The input vector to apply activation function over.
    slope:
        slope of the line that provides output for negative inputs

    Returns
        Value after leakyrelu is applied on x
    """

    if IS_CUDA :
        try :
            x_gpu = cp.asarray(x)
            res = cp.where(x_gpu > 0, x_gpu, cp.multiply(leakyrelu_slope, x_gpu))
            return cp.asnumpy(res)
        except :
            pass

    return np.where(x > 0, x, np.multiply(leakyrelu_slope, x))

def softmax(x : np.ndarray, **kwargs) -> np.ndarray :
    """SoftMax activation function
    
    This function takes a vector as input
    and changes them to probabilities based
    on their values with respect to the
    vector itself.

    Range: (0, 1)

    Args
        x:
            The input vector to apply activation function over.

    Returns
        Value after softmax is applied on x

    WARNING: Not available at the moment
    """

    if IS_CUDA :
        try :
            x_gpu = cp.asarray(x)
            res = cp.exp(x_gpu) / cp.sum(cp.exp(x_gpu))
            return cp.asnumpy(res)
        except :
            pass

    res = np.exp(x) / np.sum(np.exp(x))
    return res



def get(func : str) :
    """Helper function to get an activation function

    Return the appropriate activation function
    depending on the given string

    Args
        func:
            Query string for the requested activation function

    Returns
        Appropriate function
    """
    # TODO : handle wrong inputs
    if not isinstance(func, str) :
        ...

    func = func.strip().lower()

    if func == "sigmoid" :
        return sigmoid
    elif func == "tanh" :
        return tanh
    elif func == "relu" :
        return relu
    elif func == "leakyrelu" :
        return leakyrelu
    # elif func == "softmax" :
    #     return softmax