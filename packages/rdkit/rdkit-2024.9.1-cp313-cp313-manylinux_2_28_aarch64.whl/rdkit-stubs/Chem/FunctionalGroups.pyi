from __future__ import annotations
import os as os
from rdkit import Chem
from rdkit import RDConfig
import re as re
import typing
import weakref as weakref
__all__ = ['BuildFuncGroupHierarchy', 'Chem', 'CreateMolFingerprint', 'FGHierarchyNode', 'FuncGroupFileParseError', 'RDConfig', 'groupDefns', 'hierarchy', 'lastData', 'lastFilename', 'os', 're', 'weakref']
class FGHierarchyNode:
    __firstlineno__: typing.ClassVar[int] = 40
    __static_attributes__: typing.ClassVar[tuple] = ('children', 'label', 'name', 'parent', 'pattern', 'rxnSmarts', 'smarts')
    children = None
    label: typing.ClassVar[str] = ''
    name: typing.ClassVar[str] = ''
    parent = None
    pattern = None
    removalReaction = None
    rxnSmarts: typing.ClassVar[str] = ''
    smarts: typing.ClassVar[str] = ''
    def __init__(self, name, patt, smarts = '', label = '', rxnSmarts = '', parent = None):
        ...
    def __len__(self):
        ...
class FuncGroupFileParseError(ValueError):
    __firstlineno__: typing.ClassVar[int] = 67
    __static_attributes__: typing.ClassVar[tuple] = tuple()
def BuildFuncGroupHierarchy(fileNm = None, data = None, force = False):
    ...
def CreateMolFingerprint(mol, hierarchy):
    ...
def _SetNodeBits(mol, node, res, idx):
    ...
groupDefns: dict = {}
hierarchy = None
lastData = None
lastFilename = None
