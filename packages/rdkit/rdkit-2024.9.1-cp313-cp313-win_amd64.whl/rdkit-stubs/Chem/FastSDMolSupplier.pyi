from __future__ import annotations
from rdkit import Chem
import rdkit.Chem.rdmolfiles
import sys as sys
import typing
import warnings as warnings
__all__ = ['Chem', 'FastSDMolSupplier', 'sys', 'warnings']
class FastSDMolSupplier(rdkit.Chem.rdmolfiles.SDMolSupplier):
    __firstlineno__: typing.ClassVar[int] = 20
    __static_attributes__: typing.ClassVar[tuple] = tuple()
__warningregistry__: dict = {'version': 4}
