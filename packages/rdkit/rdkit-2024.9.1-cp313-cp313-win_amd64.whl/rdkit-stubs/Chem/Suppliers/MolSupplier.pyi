"""
Supplies an abstract class for working with sequences of molecules

"""
from __future__ import annotations
import typing
__all__ = ['MolSupplier']
class MolSupplier:
    """
    we must, at minimum, support forward iteration
    
      
    """
    __firstlineno__: typing.ClassVar[int] = 15
    __static_attributes__: typing.ClassVar[tuple] = tuple()
    def NextMol(self):
        """
        Must be implemented in child class
        
            
        """
    def Reset(self):
        ...
    def __init__(self):
        ...
    def __iter__(self):
        ...
    def __next__(self):
        ...
    def next(self):
        ...
