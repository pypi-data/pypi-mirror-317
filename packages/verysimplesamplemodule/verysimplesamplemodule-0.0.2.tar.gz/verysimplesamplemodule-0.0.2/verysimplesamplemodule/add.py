from typing import List

""" This module provides a function to add multiple values together.
"""


def add(*args: List[int]) -> int:
    """
    Adds multiple values together.

    Parameters:
    *args (int or float): A variable number of arguments to be added.

    Returns:
    int or float: The sum of all the arguments.

    Example:
    >>> add(1, 2, 3)
    6
    """
    return sum(args)


def add():
    return None