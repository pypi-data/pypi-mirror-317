"""Several common layers used in Neural Networks"""

import numpy as np
import cupy as cp

from shamboflow import IS_CUDA
from shamboflow.engine.base_layers import BaseLayer
from shamboflow.engine.activations import get

class Dense(BaseLayer) :
    """A Simple 1D layer

    A Dense layer is a simple 1D layer
    that just has a given number of
    neurons. Its the most common
    and basic layer.

    Attributes
        size: The number of neurons in the layer
        bias: An array of bias values for a neuron
        activation: The activation function to apply to this layer
        output: An array of output values after applying activation function
    
    """

    def __init__(self, size : int, activation : str = None, **kwargs) -> None:
        """Constructor for Dense Layer

        Args
            size:
                The number of neurons in the layer
            activation:
                The activation function to use for the layer. Available => `sigmoid`, `tanh`, `relu`, `leakyrelu`

        Keyword Args
            leakyrelu_slope:
                The slope value if leakyrelu is used as the activation function
        """
        super().__init__("Dense", activation != None)

        self.size : int = size
        """Size of the layer"""
        if activation != None :
            self.activation = get(activation)
            self.activation_str = activation

        if "leakyrelu_slope" in kwargs : 
            self.leakyrelu_slope = kwargs.get("leakyrelu_slope")
        

    def build(self) -> None:
        """Overidden Build method

        This method initializes the bias and output data array.
        """
        if IS_CUDA :
            self.bias_array = cp.random.uniform(-0.5, 0.5, self.size)
            self.output_array = cp.zeros(self.size)
        else :
            self.bias_array = np.random.uniform(-0.5, 0.5, self.size)
            self.output_array = np.zeros(self.size)

        super().build()
    
    def compute(self, input : np.ndarray) -> np.ndarray :
        """Method to perform computation on data

        This method accepts an input vector
        that is the output vector of the
        previous layer in the network. Then
        output values of this layer is calculated.

        The input values are simply added with the
        bias and then passed through the activation
        function.

        Args
            input:
                The input vector
        
        Returns
            The output vector after computaion
        
        """

        if not self.trainable :
            self.output_array = input
            return self.output_array

        if IS_CUDA :
            input_gpu = cp.asarray(input)
            self.midway = cp.add(input_gpu, self.bias_array)
            self.output_array = self.activation(cp.asnumpy(self.midway), leakyrelu_slope=self.leakyrelu_slope)
            return self.output_array

        self.midway = np.add(input, self.bias_array)
        self.output_array = self.activation(self.midway, leakyrelu_slope=self.leakyrelu_slope)
        return self.output_array