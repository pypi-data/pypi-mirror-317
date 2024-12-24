"""Base class file for callback methods"""

class BaseCallback :
    """Callback methods base class

    CallBack methods are those methods which
    are called at the end of each epochs to
    perform certain tasks.

    This is the base class for such callbacks.
    All callbacks need to inherit from this
    and implement the call method.
    
    """

    def __init__(self) -> None:
        pass

    def run(self) -> None :
        """Method that runs after each epoch

        Every subclass needs to implement this method
        
        """
        pass