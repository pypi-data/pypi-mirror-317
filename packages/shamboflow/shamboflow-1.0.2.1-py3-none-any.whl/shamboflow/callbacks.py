"""A collection of common callback functions"""

from colorama import Fore, Back, Style

from shamboflow.engine.base_callback import BaseCallback
from shamboflow.engine.base_models import BaseModel

class EarlyStopping(BaseCallback) :
    """Early Stopper

    This callback method monitors a given
    metric and then stops the training
    early if the metric doesn't improve
    for a given amount of time
    
    """

    def __init__(self, monitor : str = 'loss', patience : int = 10, verbose : bool = False, **kwargs) -> None :
        """Initialize

        Args
            monitor:
                The metric to monitor. It is one of the 4: ``loss``, ``acc``, ``val_loss``, ``val_acc``
            patience:
                How many epoch to monitor before stopping
            verbose:
                Log callback function logs
        
        """

        self._monitor = monitor
        self._patience = patience
        self._verbose = verbose

        self._metric_old = 0.0
        self._patience_ctr = 0

    def run(self, model : BaseModel) -> None:
        """The callback method that will be called after each epoch
        
        Args
            model: The model on which callback wil be called
        """

        if self._monitor in ('val_loss', 'val_acc') :
            if not model.has_validation_data :
                self._monitor = self._monitor.removeprefix('val_')

        current_metric = model.metrics[self._monitor]
        if model.current_epoch == 0 :
            self._metric_old = current_metric
            return
        
        if 'loss' in self._monitor :
            if current_metric >= self._metric_old :
                self._patience_ctr += 1

                if self._verbose :
                    print(f"[EarlyStopping] : {self._monitor} has not improved for the past {self._patience_ctr} epochs.")

                if self._patience_ctr == self._patience :
                    print(Back.RED + Fore.WHITE + f"Early Stopping, {self._monitor} has not improved for past {self._patience} epochs")
                    print(Style.RESET_ALL)
                    model.stop()
            else :
                self._patience_ctr = 0
        else :
            if current_metric <= self._metric_old :
                self._patience_ctr += 1

                if self._verbose :
                    print(f"[EarlyStopping] : {self._monitor} has not improved for the past {self._patience_ctr} epochs.")
                    
                if self._patience_ctr == self._patience :
                    print(Back.RED + Fore.WHITE + f"Early Stopping, {self._monitor} has not improved for past {self._patience} epochs")
                    print(Style.RESET_ALL)
                    model.stop()
            else :
                self._patience_ctr = 0

        self._metric_old = current_metric


class ReduceLROnPlateau(BaseCallback) :
    """Reduce Learning Rate on Plateau callback
    
    This callback function monitors a
    given metric for a set amount of
    iterations and reduces the learning
    rate if the metric doesn't improve
    for the given duration.
    """

    def __init__(self, monitor : str = 'loss', patience : int = 10, factor : float = 0.9, min_val : float = 1e-10, verbose : bool = False, **kwargs) -> None :
        """Initialize
        
        Args
            monitor:
                The metric to monitor. It is one of the 4: ``loss``, ``acc``, ``val_loss``, ``val_acc``
            patience:
                How many epoch to monitor before stopping
            factor:
                fraction to which the learning rate will be lowered to. Note - This is not by how much to reduce but how much to reduce to
            min_val:
                Min possible learning rate
            verbose:
                Log callback function logs
        """

        self._monitor = monitor
        self._patience = patience
        self._factor = factor
        self._min_val = min_val
        self._verbose = verbose

        self._metric_old = 0.0
        self._patience_ctr = 0

    def run(self, model : BaseModel) -> None:
        """The callback method that will be called after each epoch
        
        Args
            model: The model on which callback wil be called
        """

        if self._monitor in ('val_loss', 'val_acc') :
            if not model.has_validation_data :
                self._monitor = self._monitor.removeprefix('val_')

        current_metric = model.metrics[self._monitor]
        if model.current_epoch == 0 :
            self._metric_old = current_metric
            return
        
        if 'loss' in self._monitor :
            if current_metric >= self._metric_old :
                self._patience_ctr += 1

                if self._verbose :
                    print(f"[ReduceLROnPlateau] : {self._monitor} has not improved for the past {self._patience_ctr} epochs.")

                if self._patience_ctr == self._patience :
                    new_LR = self._factor * model.learning_rate
                    model.learning_rate = new_LR if new_LR > self._min_val else model.learning_rate

                    print(Back.RED + Fore.WHITE + f"Reducing Learning Rate, {self._monitor} has not improved for past {self._patience} epochs. New Learning rate is {model.learning_rate}")
                    print(Style.RESET_ALL)
            else :
                self._patience_ctr = 0
        else :
            if current_metric <= self._metric_old :
                self._patience_ctr += 1

                if self._verbose :
                    print(f"[ReduceLROnPlateau] : {self._monitor} has not improved for the past {self._patience_ctr} epochs.")
                    
                if self._patience_ctr == self._patience :
                    new_LR = self._factor * model.learning_rate
                    model.learning_rate = new_LR if new_LR > self._min_val else model.learning_rate

                    print(Back.RED + Fore.WHITE + f"Reducing Learning Rate, {self._monitor} has not improved for past {self._patience} epochs. New Learning rate is {model.learning_rate}")
                    print(Style.RESET_ALL)
            else :
                self._patience_ctr = 0

        self._metric_old = current_metric

class ModelCheckpoint(BaseCallback) :
    """Model Checkpointing
    
    This callback function monitors a
    metric and saves the instance of model
    to disk at every epoch or on a condition
    """

    def __init__(self, save_path : str = "model.ckpt", monitor : str = 'loss', save_best_only : bool = True, verbose : bool = False, **kwargs) -> None :
        """Initialize
        
        Args
            save_path:
                Save path for the model
            monitor:
                The metric to monitor. It is one of the 4: ``loss``, ``acc``, ``val_loss``, ``val_acc``
            save_best_only:
                whether to save only the best model according to the monitor
            verbose:
                Log callback function logs

        """

        self._save_path = save_path
        self._monitor = monitor
        self._save_best = save_best_only
        self._verbose = verbose

        self._metric_old = 0.0

    def run(self, model : BaseModel) -> None:
        """The callback method that will be called after each epoch
        
        Args
            model: The model on which callback wil be called
        """

        if not self._save_best :
            if self._verbose :
                print(f"[ModelCheckpoint] : Saving to {self._save_path}")
            model.save(self._save_path)
            return

        if self._monitor in ('val_loss', 'val_acc') :
            if not model.has_validation_data :
                self._monitor = self._monitor.removeprefix('val_')

        current_metric = model.metrics[self._monitor]
        if model.current_epoch == 0 :
            self._metric_old = current_metric
            return
        
        if 'loss' in self._monitor :
            if current_metric < self._metric_old :
                if self._verbose :
                    print(f"[ModelCheckpoint] : Metric has improved. Saving to {self._save_path}")
                model.save(self._save_path)
        else :
            if current_metric > self._metric_old :
                if self._verbose :
                    print(f"[ModelCheckpoint] : Metric has improved. Saving to {self._save_path}")
                model.save(self._save_path)

        self._metric_old = current_metric