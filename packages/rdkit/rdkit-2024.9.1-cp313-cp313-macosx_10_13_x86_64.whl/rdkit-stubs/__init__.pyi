from __future__ import annotations
import logging as logging
import sys as sys
import typing
from .rdBase import *
__all__ = ['VECT_WRAPS', 'VectIter', 'log_handler', 'logger', 'logging', 'name', 'object', 'rdBase', 'sys']
class VectIter:
    __firstlineno__: typing.ClassVar[int] = 43
    __static_attributes__: typing.ClassVar[tuple] = ('l', 'pos', 'vect')
    def __init__(self, vect):
        ...
    def __iter__(self):
        ...
    def __next__(self):
        ...
def __vect__iter__(vect):
    ...
VECT_WRAPS: set = {'MatchTypeVect', 'UnsignedLong_Vect', 'VectorOfStringVectors', 'VectSizeT'}
__version__: str = '2024.09.1'
log_handler: logging.StreamHandler  # value = <StreamHandler <stderr> (NOTSET)>
logger: logging.Logger  # value = <Logger rdkit (WARNING)>
name: str = '__file__'
object: str = '/Users/runner/work/rdkit-pypi/rdkit-pypi/build/temp.macosx-10.9-x86_64-cpython-313/rdkit_install/lib/python3.13/site-packages/rdkit/rdBase.so'
