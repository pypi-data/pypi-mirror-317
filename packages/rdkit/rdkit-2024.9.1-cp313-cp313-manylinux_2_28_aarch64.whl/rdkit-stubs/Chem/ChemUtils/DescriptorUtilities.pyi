"""

Collection of utilities to be used with descriptors

"""
from __future__ import annotations
import math as math
import typing
__all__ = ['VectorDescriptorNamespace', 'VectorDescriptorWrapper', 'math', 'setDescriptorVersion']
class VectorDescriptorNamespace(dict):
    __firstlineno__: typing.ClassVar[int] = 29
    __static_attributes__: typing.ClassVar[tuple] = tuple()
    def __init__(self, **kwargs):
        ...
class VectorDescriptorWrapper:
    """
    Wrap a function that returns a vector and make it seem like there
    is one function for each entry.  These functions are added to the global
    namespace with the names provided
    """
    __firstlineno__: typing.ClassVar[int] = 35
    __static_attributes__: typing.ClassVar[tuple] = ('func', 'func_key', 'names', 'namespace')
    def __init__(self, func, names, version, namespace):
        ...
    def _get_key(self, index):
        ...
    def call_desc(self, mol, index):
        ...
def setDescriptorVersion(version = '1.0.0'):
    """
    Set the version on the descriptor function.
    
    Use as a decorator 
    """
