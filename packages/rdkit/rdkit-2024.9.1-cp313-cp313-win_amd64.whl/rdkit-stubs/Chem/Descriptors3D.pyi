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
descList: list  # value = [('PMI1', <function <lambda> at 0x000002162E9F96C0>), ('PMI2', <function <lambda> at 0x000002162E9F9E40>), ('PMI3', <function <lambda> at 0x000002162E9F9EE0>), ('NPR1', <function <lambda> at 0x000002162E9F9F80>), ('NPR2', <function <lambda> at 0x000002162E9FA020>), ('RadiusOfGyration', <function <lambda> at 0x000002162E9FA0C0>), ('InertialShapeFactor', <function <lambda> at 0x000002162E9FA160>), ('Eccentricity', <function <lambda> at 0x000002162E9FA200>), ('Asphericity', <function <lambda> at 0x000002162E9FA2A0>), ('SpherocityIndex', <function <lambda> at 0x000002162E9FA340>), ('PBF', <function <lambda> at 0x000002162E9FA3E0>)]
