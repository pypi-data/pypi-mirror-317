class _TypeError(TypeError):
    def __init__(self, name: str, expected: str) -> None:
        """_TypeError

        Args:
            name (str): Name of the variable.
            expected (str): Expected type (which wasn't recieved).

        Raises:
            _TypeError: If 'name' or 'expected' aren't a string.
        """        
        if not isinstance(name, str):
            raise _TypeError("name", "str")
        
        if not isinstance(expected, str):
            raise _TypeError("expected", "str")
        
        super().__init__(f"{name} must be type {expected}.")

class _NotEnoughError(IndexError):
    def __init__(self, name: str):
        """_NotEnoughtError

        Args:
            name (str): Name of the not available type

        Raises:
            _TypeError: In case that name is not a string
        """        
        if not isinstance(name, str):
            raise _TypeError("name", "str")
        
        super().__init__(f"Not available {name} to read.")

class _MoreThanExpectedArgsError(SyntaxError):
    def __init__(self, name: str, expected: int, recieved: int):
        """_MoreThanExpectedArgsErroor

        Args:
            name (str): Function name where error was raised
            expected (int): Amount of arguments expected
            recieved (int): Amount of arguments recieved
        """        
        if not isinstance(name, str):
            raise _TypeError("name", "str")
        
        if not isinstance(expected, int):
            raise _TypeError("expected", "int")
        
        if not isinstance(recieved, int):
            raise _TypeError("recieved", "int")
        
        super().__init__(f"Function {name} expected {expected} arguments but recieved {recieved} arguments.")