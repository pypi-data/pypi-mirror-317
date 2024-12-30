"""
utility functions to help work with files

"""
from __future__ import annotations
import typing
__all__ = ['MoveToMatchingLine', 'NoMatchFoundError']
class NoMatchFoundError(RuntimeError):
    __firstlineno__: typing.ClassVar[int] = 10
    __static_attributes__: typing.ClassVar[tuple] = tuple()
def MoveToMatchingLine(inFile, matchStr, fullMatch = 0):
    """
    skip forward in a file until a given string is found
    
    **Arguments**
    
      - inFile: a file object (or anything supporting a _readline()_ method)
    
      - matchStr: the string to search for
    
      - fullMatch: if nonzero, _matchStr_ must match the entire line
    
    **Returns**
    
      the matching line
    
    **Notes:**
    
      - if _matchStr_ is not found in the file, a NoMatchFound exception
        will be raised
    
    """
