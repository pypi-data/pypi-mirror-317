"""
This module provides a function to subtract multiple numbers.
"""

def substract(*args):
    """
    Subtracts all subsequent arguments from the first argument.

    Parameters:
    *args (int or float): A variable number of arguments to be subtracted.

    Returns:
    int or float: The result of the subtraction if more than one argument is provided.
                  If only one argument is provided, returns the argument itself.

    Example:
    >>> substract(5, 1, 1)
    3
    """
    return args[0] - sum(args[1:]) if len(args) > 1 else args

print(substract(5, 1, 1))