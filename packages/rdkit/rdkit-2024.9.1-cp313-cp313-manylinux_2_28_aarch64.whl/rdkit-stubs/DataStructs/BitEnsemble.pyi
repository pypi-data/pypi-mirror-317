"""
#DOC


"""
from __future__ import annotations
import typing
__all__ = ['BitEnsemble']
class BitEnsemble:
    """
    used to store a collection of bits and score
    BitVects (or signatures) against them.
    
    """
    __firstlineno__: typing.ClassVar[int] = 17
    __static_attributes__: typing.ClassVar[tuple] = ('_bits')
    def AddBit(self, bit):
        ...
    def GetBits(self):
        ...
    def GetNumBits(self):
        ...
    def ScoreWithIndex(self, other):
        """
        other must support __getitem__() 
        """
    def ScoreWithOnBits(self, other):
        """
        other must support GetOnBits() 
        """
    def SetBits(self, bits):
        ...
    def __init__(self, bits = None):
        ...
