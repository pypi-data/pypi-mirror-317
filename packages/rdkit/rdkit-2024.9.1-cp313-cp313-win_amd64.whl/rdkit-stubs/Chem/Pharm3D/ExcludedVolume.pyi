from __future__ import annotations
import typing
__all__ = ['ExcludedVolume']
class ExcludedVolume:
    __firstlineno__: typing.ClassVar[int] = 12
    __static_attributes__: typing.ClassVar[tuple] = ('exclusionDist', 'featInfo', 'index', 'pos')
    def __init__(self, featInfo, index = -1, exclusionDist = 3.0):
        """
        
        featInfo should be a sequence of ([indices],min,max) tuples
        
        """
