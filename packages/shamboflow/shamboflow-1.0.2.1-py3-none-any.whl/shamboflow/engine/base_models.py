"""Base class for models"""

import numpy as np

from shamboflow.engine.base_layers import BaseLayer

class BaseModel :
    """The Base class for models
    
    All other models need to
    inherit from this class.
    It provides a template with
    all the methods a model will
    need to execute.

    Attributes
        layers:
            A list of layers present in the model in the order from input to output
        weights:
            A list of all weight matrices for the layers in the model
        loss:
            The loss/cost function to use calculate error of the model at a given state
        train_data_x:
            The training data or features
        train_data_y:
            Training features' corresponding labels

    And more attributes

    """

    def __init__(self, **kwargs) -> None:
        """Initialize the required attributes.

        Also optionally takes in a list of
        layers as a parameter.

        Keyword Args
            layers: It takes a list of layers and them to the model
        
        """

        self.layers : list[BaseLayer] = []
        """A list of layers in the model"""
        self.weights : list[np.ndarray] = []
        """A list of all weights between each layers"""
        self.loss = None
        """The loss function used by the model"""
        self.loss_str : str = ""
        """The name of the loss function used"""
        self.learning_rate : float = 0.0
        """The learning rate of the model"""
        self.train_data_x : np.ndarray = None
        """The feature list of the dataset"""
        self.train_data_y : np.ndarray = None
        """The labels for each data in the dataset"""
        self.validation_x : np.ndarray = None
        """Features of validation set"""
        self.validation_y : np.ndarray = None
        """Labels of the validation set"""
        self.has_validation_data : bool = False
        """Boolean flag fo if the the model has validation data"""
        self.test_data_x : np.ndarray = None
        """Features of the test dataset"""
        self.test_data_y : np.ndarray = None
        """Labels for the test dataset"""
        self.epochs : int = None
        """Number of epochs to train for"""
        self.callbacks : list = []
        """A list of callback functions"""

        self.error_val : float = 0.0
        """The loss value of the model at any instance"""
        self.accuracy_val : float = 0.0
        """The accuracy value of the model at any instance"""

        self.metrics : dict = {'loss' : 0.0, 'acc' : 0.0, 'val_loss' : 0.0, 'val_acc' : 0.0}
        """A dictionary of metrics for the model. Includes ``loss``, ``acc``, ``val_loss``, ``val_acc``"""
        self.current_epoch : int = 0
        """The current epoch of the model during training"""
        self.is_fitting : bool = True
        """Is the model training right now"""

        self.parameters : int = 0
        """Amount of trainable parameters in the model"""

        self.is_compiled : bool = False
        """Has the model been compiled"""

        if "layers" in kwargs :
            layers_arg = kwargs.get("layers")
            for layer in layers_arg :
                self.add(layer)


    def add(self, layer : BaseLayer) -> None :
        """Method to add layers to the model

        Args
            layer:
                layer to add to the model
        
        """
        self.layers.append(layer)

    def compile(self) -> None :
        """Model compilation method
        
        To be implemented in child
        """
        pass

    def fit(self) -> None :
        """Method to train the model on data
        
        To be implemented in child
        """
        pass

    def stop(self) -> None :
        """Method to stop the training"""
        self.is_fitting = False

    def summary(self) -> None :
        """Prints a summary of the model with all necessary details"""
        pass

    def save(self) -> None :
        """Saves the model to the disk"""
        pass
    
    def evaluate(self) -> None :
        """Evaluates metrics based on a Test dataset"""
        pass
    
    def predict(self) -> None :
        """Calculate inference using the trained model"""
        pass