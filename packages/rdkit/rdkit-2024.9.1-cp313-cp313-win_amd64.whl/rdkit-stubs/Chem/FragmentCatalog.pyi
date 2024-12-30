from __future__ import annotations
from rdkit import Chem
from rdkit.Chem.rdfragcatalog import FragCatGenerator
from rdkit.Chem.rdfragcatalog import FragCatParams
from rdkit.Chem.rdfragcatalog import FragCatalog
from rdkit.Chem.rdfragcatalog import FragFPGenerator
import sys as sys
import typing
__all__ = ['BitGainsInfo', 'BuildAdjacencyList', 'Chem', 'FragCatGenerator', 'FragCatParams', 'FragCatalog', 'FragFPGenerator', 'GetMolsMatchingBit', 'ProcessGainsFile', 'message', 'sys']
class BitGainsInfo:
    __firstlineno__: typing.ClassVar[int] = 21
    __static_attributes__: typing.ClassVar[tuple] = tuple()
    description: typing.ClassVar[str] = ''
    gain: typing.ClassVar[float] = 0.0
    id: typing.ClassVar[int] = -1
    nPerClass = None
def BuildAdjacencyList(catalog, bits, limitInclusion = 1, orderLevels = 0):
    ...
def GetMolsMatchingBit(mols, bit, fps):
    ...
def ProcessGainsFile(fileName, nToDo = -1, delim = ',', haveDescriptions = 1):
    ...
def message(msg, dest = ...):
    ...
