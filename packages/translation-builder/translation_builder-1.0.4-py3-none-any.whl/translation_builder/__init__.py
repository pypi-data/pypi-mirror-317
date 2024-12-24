"""
This module provides a class for building translation file with classes
"""
__all__ = ("InvalidNameError", "DuplicateNameError", "ClassBuilder", "__version__")

__version__ = "1.0.4"

from .errors import InvalidNameError, DuplicateNameError
from ._builder import ClassBuilder
