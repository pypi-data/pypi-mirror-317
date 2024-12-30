"""

Supplies a class for working with molecules from databases
"""
from __future__ import annotations
from rdkit import Chem
import rdkit.Chem.Suppliers.MolSupplier
from rdkit.Chem.Suppliers.MolSupplier import MolSupplier
import sys as sys
import typing
__all__ = ['Chem', 'DbMolSupplier', 'ForwardDbMolSupplier', 'MolSupplier', 'RandomAccessDbMolSupplier', 'sys', 'warning']
class DbMolSupplier(rdkit.Chem.Suppliers.MolSupplier.MolSupplier):
    """
    
    new molecules come back with all additional fields from the
    database set in a "_fieldsFromDb" data member
    
    """
    __firstlineno__: typing.ClassVar[int] = 23
    __static_attributes__: typing.ClassVar[tuple] = ('_colNames', '_data', '_numProcessed', 'molCol', 'molFmt', 'nameCol', 'transformFunc')
    def GetColumnNames(self):
        ...
    def _BuildMol(self, data):
        ...
    def __init__(self, dbResults, molColumnFormats = {'SMILES': 'SMI', 'SMI': 'SMI', 'MOLPKL': 'PKL'}, nameCol = '', transformFunc = None, **kwargs):
        """
        
        
        DbResults should be a subclass of Dbase.DbResultSet.DbResultBase
        
        """
class ForwardDbMolSupplier(DbMolSupplier):
    """
    DbMol supplier supporting only forward iteration
    
    
    new molecules come back with all additional fields from the
    database set in a "_fieldsFromDb" data member
    
    """
    __firstlineno__: typing.ClassVar[int] = 102
    __static_attributes__: typing.ClassVar[tuple] = ('_dataIter')
    def NextMol(self):
        """
        
        
        NOTE: this has side effects
        
        """
    def Reset(self):
        ...
    def __init__(self, dbResults, **kwargs):
        """
        
        
        DbResults should be an iterator for Dbase.DbResultSet.DbResultBase
        
        """
class RandomAccessDbMolSupplier(DbMolSupplier):
    __firstlineno__: typing.ClassVar[int] = 141
    __static_attributes__: typing.ClassVar[tuple] = ('_pos')
    def NextMol(self):
        ...
    def Reset(self):
        ...
    def __getitem__(self, idx):
        ...
    def __init__(self, dbResults, **kwargs):
        """
        
        
        DbResults should be a Dbase.DbResultSet.RandomAccessDbResultSet
        
        """
    def __len__(self):
        ...
def warning(msg, dest = ...):
    ...
