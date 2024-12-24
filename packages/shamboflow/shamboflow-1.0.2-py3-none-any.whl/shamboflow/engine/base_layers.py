"""Base class for layers"""

import numpy as np

class BaseLayer :
    """The base class for layers to inherit from.

    A layer is an object that is a part of
    the neural network. It performs calculations
    on neurons or neurons present in it
    commonly. It can also not have computable
    neurons, instead can also be used to filter
    data from previous layers.

    Attributes
        name:
            The name of the layer
        trainable:
            Is the layer trainable
        is_built:
            Is the layer built and initialized
    """

    def __init__(self, name : str, trainable : bool = True) -> None:
        """Constructor for the base layer class

        Args
            name:
                Name of the layer
            trainable:
                Is the layer trainable. Default is True
        
        """
        self.name : str = name
        """Name of the layer"""
        self.trainable : bool = trainable
        """Is the layer trainable"""
        self.is_built : bool = False
        """has the layer been built and compiled"""

        self.bias_array : np.ndarray = None
        """Bias values of the layer"""
        self.output_array : np.ndarray = None
        """Output matrix of the layer"""
        self.midway : np.ndarray = None
        """Output value before applying avtivation function"""
        self.error_array : np.ndarray = None
        """Error values of the layer"""
        self.leakyrelu_slope : float = 0.0
        """Slope value if using leakyrelu activation function"""

        self.activation = None
        """Activation function used by the layer"""
        self.activation_str : str = None
        """The name of the activation function"""

    def build(self) -> None :
        """Method to build and initialize the layer.

        This method is to be overidden by child
        classes to build them by their own logic.
        
        """
        self.is_built = True

    def compute(self) -> None :
        """Method to compute various parameter
        
        This method is to be implemented in inherited classes
        """
        pass