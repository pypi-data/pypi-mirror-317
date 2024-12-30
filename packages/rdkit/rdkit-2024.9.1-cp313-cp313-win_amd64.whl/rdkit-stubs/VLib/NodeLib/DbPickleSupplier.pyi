from __future__ import annotations
import os as os
import pickle as pickle
from rdkit import RDConfig
import rdkit.VLib.Supply
from rdkit.VLib.Supply import SupplyNode
import sys as sys
import typing
__all__ = ['DbPickleSupplyNode', 'GetNode', 'RDConfig', 'SupplyNode', 'os', 'pickle', 'sys']
class DbPickleSupplyNode(rdkit.VLib.Supply.SupplyNode):
    """
    Supplies pickled objects from a db result set:
    
    Sample Usage:
      >>> from rdkit.Dbase.DbConnection import DbConnect
    
    """
    __firstlineno__: typing.ClassVar[int] = 169
    __static_attributes__: typing.ClassVar[tuple] = ('_dbResults', '_supplier')
    def __init__(self, cursor, cmd, binaryCol, **kwargs):
        ...
    def next(self):
        """
        
        
            
        """
    def reset(self):
        ...
def GetNode(dbName, tableName):
    ...
def _test():
    ...
_dataSeq = None
