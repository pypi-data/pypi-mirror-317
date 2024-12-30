from __future__ import annotations
from rdkit.Chem.FeatMaps import FeatMapPoint
from rdkit.Chem.FeatMaps import FeatMaps
from rdkit import Geometry
import re as re
import typing
__all__ = ['FeatMapParseError', 'FeatMapParser', 'FeatMapPoint', 'FeatMaps', 'Geometry', 're']
class FeatMapParseError(ValueError):
    __firstlineno__: typing.ClassVar[int] = 36
    __static_attributes__: typing.ClassVar[tuple] = tuple()
class FeatMapParser:
    __firstlineno__: typing.ClassVar[int] = 40
    __static_attributes__: typing.ClassVar[tuple] = ('_lineNum', 'data')
    data = None
    def Parse(self, featMap = None):
        ...
    def ParseFeatPointBlock(self):
        ...
    def ParseParamBlock(self):
        ...
    def SetData(self, data):
        ...
    def _NextLine(self):
        ...
    def __init__(self, file = None, data = None):
        ...
    def _parsePoint(self, txt):
        ...
