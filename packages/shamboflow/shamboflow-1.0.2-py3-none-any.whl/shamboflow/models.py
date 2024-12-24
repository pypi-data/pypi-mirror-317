"""Some common models"""

import numpy as np
import cupy as cp

from shamboflow import IS_CUDA
from shamboflow.engine.base_layers import BaseLayer
from shamboflow.engine.base_models import BaseModel
from shamboflow.engine import losses
from shamboflow.engine import d_losses, d_activations

from tqdm import tqdm, trange
from colorama import Fore, Back, Style

class Sequential(BaseModel) :
    """A simple sequential model with multiple layers one after the other
    
    This is the simplest model type
    that is commonly used. It has
    multiple layers in it sequentially
    connected by dense connected directed
    graph between neurons.

    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def add(self, layer: BaseLayer) -> None:
        return super().add(layer)

    def compile(self, loss : str, learning_rate : float = 0.001, verbose : bool = False, **kwargs) -> None:
        """Method to initialize and compile the model
        
        Initializes all the required values
        and performs required operations.

        Args
            loss:
                The loss function to use. Available => ``mean_squared_error``
            learning_rate:
                The learning_rate to use while fitting data
            verbose:
                Should progress be displayed in details

        """

        self.learning_rate = learning_rate
        self.loss_str = loss
        self.loss = losses.get(loss)

        if verbose :
            print(Fore.CYAN + "Compiling Model ...")
            print(Style.RESET_ALL + "Building layers")

        with tqdm(self.layers) as pbar :
            for layer in pbar :
                layer.build()
                self.parameters += layer.size
                if verbose :
                    pbar.update()

        if verbose :
            print(Fore.GREEN + "Finished building layers!")
            print(Style.RESET_ALL + "Generating weight matrices")
            
        for i in trange(len(self.layers) - 1) :
            size_a = self.layers[i].size
            size_b = self.layers[i+1].size

            self.parameters += size_a * size_b

            if IS_CUDA :
                weight_mat = cp.random.uniform(-0.5, 0.5, (size_a, size_b))
                self.weights.append(weight_mat)
            else :
                weight_mat = np.random.uniform(-0.5, 0.5, (size_a, size_b))
                self.weights.append(weight_mat)

        if verbose :
            print(Fore.GREEN + "Finished generating weight matrices")

        print(Fore.CYAN + "Model successfully compiled")
        print(Style.RESET_ALL)

        self.is_compiled = True


    def fit(self, train_x : np.ndarray, train_y : np.ndarray, epochs : int, **kwargs) -> None:
        """Method to train the model and fit the data

        It runs the training where the
        network does the learning.

        Args
            train_x:
                The features of the dataset
            train_y:
                The label of the dataset
            epochs:
                The number of steps to run the training for
            
            
        Keyword Args
            validation_x: validation data set features
            validation_y: validation data set labels
            callbacks:  A list of callback methods
        
        """

        if not self.is_compiled :
            print(Fore.WHITE + Back.RED + "Model not compiled ! Compile the model first.")
            print(Style.RESET_ALL)
            return

        self.train_data_x = train_x
        self.train_data_y = train_y
        self.epochs = epochs

        if 'validation_x' in kwargs and 'validation_y' in kwargs :
            self.has_validation_data = True
            self.validation_x = kwargs['validation_x']
            self.validation_y = kwargs['validation_y']

        if 'callbacks' in kwargs :
            self.callbacks = kwargs['callbacks']

        num_rows = self.train_data_x.shape[0] - 1

        while self.is_fitting and self.current_epoch < self.epochs :

            with tqdm(total=num_rows + 1) as pbar :
                def row_iter(x, idx) :
                    num_layer = -1

                    # Forward propagation
                    for layer in self.layers :
                        num_layer += 1
                        if num_layer == 0 :
                            layer.compute(input = x)
                            continue

                        if IS_CUDA :
                            op_gpu = cp.asarray(self.layers[num_layer - 1].output_array)
                            weight_gpu = self.weights[num_layer - 1]
                            layer.compute(cp.asnumpy(cp.matmul(op_gpu, weight_gpu)))
                        else :
                            op = self.layers[num_layer - 1].output_array
                            weight = self.weights[num_layer - 1]
                            layer.compute(np.matmul(op, weight))
                    
                    self.error_val = self.loss(self.layers[num_layer].output_array, self.train_data_y[idx])
                    acc = np.subtract(self.train_data_y[idx], self.layers[num_layer].output_array)
                    self.accuracy_val = (self.layers[num_layer].size - np.count_nonzero(acc)) / self.layers[num_layer].size

                    self.metrics['acc'] = self.accuracy_val
                    self.metrics['loss'] = self.error_val

                    # Validation
                    if self.has_validation_data :
                        self.evaluate(self.validation_x, self.validation_y, is_validation=True)

                    # BackPropagation
                    d_loss_fun = d_losses.get(self.loss_str)
                    d_act_fun = d_activations.get(self.layers[num_layer].activation_str)

                    if IS_CUDA :
                        ## Compute Gradients for output layer
                        d_loss_res_gpu = cp.asarray(d_loss_fun(self.layers[num_layer].output_array, self.train_data_y[idx]))
                        d_act_res_gpu = cp.asarray(d_act_fun(self.layers[num_layer].midway, leakyrelu_slope=self.layers[num_layer].leakyrelu_slope))
                        gradient_op = cp.multiply(d_loss_res_gpu, d_act_res_gpu)
                        self.layers[num_layer].error_array = gradient_op
                        weight_gradient = cp.multiply.outer(gradient_op, self.layers[num_layer - 1].output_array)
                        self.weights[num_layer - 1] = cp.add(self.weights[num_layer - 1], cp.multiply(self.learning_rate, weight_gradient).T)

                        ## Compute Gradient for output layer bias
                        # gradient_op is the bias gradient itself
                        # Adjust bias
                        self.layers[num_layer].bias_array = cp.add(self.layers[num_layer].bias_array, cp.multiply(self.learning_rate, gradient_op))

                        # Hidden layers
                        for i in range(len(self.layers) - 2, 0, -1) :
                            d_act_fun = d_activations.get(self.layers[i].activation_str)
                            error_next = self.layers[i+1].error_array
                            d_act_res_hidden = cp.asarray(d_act_fun(self.layers[i].midway, leakyrelu_slope=self.layers[i].leakyrelu_slope))
                            hidden_weight = cp.transpose(self.weights[i])
                            hidden_err_midway = cp.matmul(error_next, hidden_weight)
                            hidden_error = cp.multiply(hidden_err_midway, d_act_res_hidden)
                            self.layers[i].error_array = hidden_error

                            weight_gradient_hidden = cp.multiply.outer(hidden_error, self.layers[i-1].output_array)
                            self.weights[i-1] = cp.add(self.weights[i-1], cp.multiply(self.learning_rate, weight_gradient_hidden).T)

                            # Bias
                            self.layers[i].bias_array = cp.add(self.layers[i].bias_array, cp.multiply(self.learning_rate, hidden_error))
                        
                    else :
                        ## Compute Gradients for output layer
                        d_loss_res = d_loss_fun(self.layers[num_layer].output_array, self.train_data_y[idx])
                        d_act_res = d_act_fun(self.layers[num_layer].midway, leakyrelu_slope=self.layers[num_layer].leakyrelu_slope)
                        gradient_op = np.multiply(d_loss_res, d_act_res)
                        self.layers[num_layer].error_array = gradient_op
                        weight_gradient = np.multiply.outer(gradient_op, self.layers[num_layer - 1].output_array)
                        self.weights[num_layer - 1] = np.add(self.weights[num_layer - 1], np.multiply(self.learning_rate, weight_gradient).T)

                        ## Compute Gradient for output layer bias
                        # gradient_op is the bias gradient itself
                        # Adjust bias
                        self.layers[num_layer].bias_array = np.add(self.layers[num_layer].bias_array, np.multiply(self.learning_rate, gradient_op))

                        # Hidden layers
                        for i in range(len(self.layers) - 2, 0, -1) :
                            d_act_fun = d_activations.get(self.layers[i].activation_str)
                            error_next = self.layers[i+1].error_array
                            d_act_res_hidden = d_act_fun(self.layers[i].midway, leakyrelu_slope=self.layers[i].leakyrelu_slope)
                            hidden_weight = self.weights[i]
                            hidden_err_midway = np.matmul(error_next, hidden_weight)
                            hidden_error = np.multiply(hidden_err_midway, d_act_res_hidden)
                            self.layers[i].error_array = hidden_error

                            weight_gradient_hidden = np.multiply.outer(hidden_error, self.layers[i-1].output_array)
                            self.weights[i-1] = np.add(self.weights[i-1], np.multiply(self.learning_rate, weight_gradient_hidden).T)

                            # Bias
                            self.layers[i].bias_array = np.add(self.layers[i].bias_array, np.multiply(self.learning_rate, hidden_error))

                    pbar.set_description(f"Epoch: {self.current_epoch}")
                    pbar.set_postfix_str(f"Accuracy: {self.accuracy_val}, Loss: {self.error_val}")
                    pbar.update(1)    

                for idx, row_x in enumerate(self.train_data_x) :
                    row_iter(row_x, idx)
            
            # Call the callback methods
            for callback in self.callbacks :
                callback.run(model=self)

            self.current_epoch += 1


    def evaluate(self, x_data : np.ndarray, y_data : np.ndarray, **kwargs) -> None:
        """Method to evaluate the model with test data
        
        Args
            x_data:
                The features of the dataset
            y_data:
                The label of the dataset
            
        Keyword Args
            is_validation: Whether the model is called during validation set checking step of training
        """

        is_val = False
        if 'is_validation' in kwargs :
            is_val = kwargs['is_validation']

        num_rows = x_data.shape[0]
        test_error_val = 0.0
        test_accuracy_val = 0.0

        with tqdm(total=num_rows) as pbar :
            def row_iter(x, idx) :
                num_layer = -1
                global test_error_val
                global test_accuracy_val

                for layer in self.layers :
                    num_layer += 1
                    if num_layer == 0 :
                        layer.compute(input = x)
                        continue

                    if IS_CUDA :
                        op_gpu = cp.asarray(self.layers[num_layer - 1].output_array)
                        weight_gpu = self.weights[num_layer - 1]
                        layer.compute(cp.matmul(op_gpu, weight_gpu))
                    else :
                        op = self.layers[num_layer - 1].output_array
                        weight = self.weights[num_layer - 1]
                        layer.compute(np.matmul(op, weight))
                    
                test_error_val = self.loss(self.layers[num_layer].output_array, y_data[idx])
                acc = np.subtract(y_data[idx], self.layers[num_layer].output_array)
                test_accuracy_val = (self.layers[num_layer].size - np.count_nonzero(acc)) / self.layers[num_layer].size

                if is_val :
                    self.metrics['val_loss'] = test_error_val
                    self.metrics['val_acc'] = test_accuracy_val
                    return

                pbar.set_postfix_str(f"Accuracy: {test_accuracy_val}, Loss: {test_error_val}")
                pbar.update(1)

            for idx, row_x in enumerate(x_data) :
                row_iter(row_x, idx)

        print(f"Accuracy: {test_accuracy_val}, Error: {test_error_val}")


    def summary(self) -> None:
        """Prints a summary of the model once compiled"""

        if not self.is_compiled :
            print(Back.RED + Fore.WHITE + "Model has not been compiled.\nCompile the model first using model.compile()")
            print(Style.RESET_ALL)
            return

        print(Fore.WHITE + "Model type : " + Fore.CYAN + "Sequential\n")
        print(Fore.WHITE + "Layers: ")

        for layer in self.layers :
            print("-> " + Fore.CYAN + layer.name + Fore.WHITE + f" Neurons: {layer.size} Activation: {layer.activation_str if layer.trainable else 'Not trainable'} Trainable: {layer.trainable}")

        print(Style.RESET_ALL)
        print(f"\nTrainable Params: {self.parameters}")


    def save(self, save_path : str) -> None:
        """Method to save the model to disk
        
        Args
            save_path:
                Path to where the model will be saved, along with the name of the model file
        """

        import pickle

        with open(save_path, 'wb') as f :
            pickle.dump(self, f)
            print(f"Saved model to: {save_path}")

    def predict(self, input_x : np.ndarray) -> np.ndarray :
        """Method to predict data labels
        
        Args
            input_x:
                The features of the data to predict

        Returns
            The final output layer with the generated values
        """
        
        num_layer = -1
        pred_layers = self.layers

        for layer in pred_layers :
            num_layer += 1
            if num_layer == 0 :
                layer.compute(input = input_x)
                continue

            if IS_CUDA :
                op_gpu = cp.asarray(pred_layers[num_layer - 1].output_array)
                weight_gpu = self.weights[num_layer - 1]
                layer.compute(cp.matmul(op_gpu, weight_gpu))
            else :
                op = pred_layers[num_layer - 1].output_array
                weight = self.weights[num_layer - 1]
                layer.compute(np.matmul(op, weight))
        
        return pred_layers[num_layer].output_array
        

def load_model(path_to_model : str) -> BaseModel :
    """Method to load a model from disk
    
    Args
        path_to_model:
            path to the model file
    
    Returns
        The model object

    """

    import pickle

    with open(path_to_model, 'rb') as f :
        model = pickle.load(f)
        return model