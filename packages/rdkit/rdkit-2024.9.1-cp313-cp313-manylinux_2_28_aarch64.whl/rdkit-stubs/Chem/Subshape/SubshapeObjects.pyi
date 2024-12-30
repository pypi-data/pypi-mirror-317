from __future__ import annotations
import typing
__all__ = ['DisplaySubshape', 'DisplaySubshapeSkeleton', 'ShapeWithSkeleton', 'SkeletonPoint', 'SubshapeShape']
class ShapeWithSkeleton:
    __firstlineno__: typing.ClassVar[int] = 26
    __static_attributes__: typing.ClassVar[tuple] = ('skelPts')
    grid = None
    skelPts = None
    def __init__(self, *args, **kwargs):
        ...
    def _initMemberData(self):
        ...
class SkeletonPoint:
    __firstlineno__: typing.ClassVar[int] = 7
    __static_attributes__: typing.ClassVar[tuple] = ('featmapFeatures', 'location', 'molFeatures', 'shapeDirs', 'shapeMoments')
    featmapFeatures = None
    fracVol: typing.ClassVar[float] = 0.0
    location = None
    molFeatures = None
    shapeDirs = None
    shapeMoments = None
    def __init__(self, *args, **kwargs):
        ...
    def _initMemberData(self):
        ...
class SubshapeShape:
    __firstlineno__: typing.ClassVar[int] = 37
    __static_attributes__: typing.ClassVar[tuple] = ('shapes')
    featMap = None
    keyFeat = None
    shapes = None
    def __init__(self, *args, **kwargs):
        ...
    def _initMemberData(self):
        ...
def DisplaySubshape(viewer, shape, name, showSkelPts = True, color = (1, 0, 1)):
    ...
def DisplaySubshapeSkeleton(viewer, shape, name, color = (1, 0, 1), colorByOrder = False):
    ...
def _displaySubshapeSkelPt(viewer, skelPt, cgoNm, color):
    ...
