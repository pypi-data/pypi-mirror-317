"""
Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
    Compute all 3D descriptors of a molecule
    
    Arguments:
    - mol: the molecule to work with
    - confId: conformer ID to work with. If not specified the default (-1) is used
    
    Return:
    
    dict
        A dictionary with decriptor names as keys and the descriptor values as values
    
    raises a ValueError 
        If the molecule does not have conformers
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0xffff7eb76700>), ('PMI2', <function <lambda> at 0xffff7eb768e0>), ('PMI3', <function <lambda> at 0xffff7eb76f20>), ('NPR1', <function <lambda> at 0xffff7eb76fc0>), ('NPR2', <function <lambda> at 0xffff7eb77060>), ('RadiusOfGyration', <function <lambda> at 0xffff7eb77100>), ('InertialShapeFactor', <function <lambda> at 0xffff7eb771a0>), ('Eccentricity', <function <lambda> at 0xffff7eb77240>), ('Asphericity', <function <lambda> at 0xffff7eb772e0>), ('SpherocityIndex', <function <lambda> at 0xffff7eb77380>), ('PBF', <function <lambda> at 0xffff7eb77420>)]
