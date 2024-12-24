"""
This module contains custom exceptions that are used in the translation builder
"""


class InvalidNameError(Exception):
    """
    Indicates the content of invalid characters for variable names

    :param name: The name of the variable that contains invalid characters
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return "Variable contains invalid characters: " + self.name


class DuplicateNameError(Exception):
    """
    Indicates that a variable name is already in use

    :param name: The name of the variable that is already in use
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return "Variable name is already in use: " + self.name
