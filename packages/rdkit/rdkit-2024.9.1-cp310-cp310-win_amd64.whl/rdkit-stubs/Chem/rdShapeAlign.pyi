from __future__ import annotations
import typing
__all__ = ['AlignMol', 'FloatVector', 'PrepareConformer', 'ShapeInput']
class FloatVector(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::vector<float,class std::allocator<float> > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::vector<float,class std::allocator<float> > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::vector<float,class std::allocator<float> > & __ptr64>,struct _object * __ptr64)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_value_policy<struct boost::python::return_by_value,struct boost::python::default_call_policies>,class std::_Vector_iterator<class std::_Vector_val<struct std::_Simple_types<float> > > > __iter__(struct boost::python::back_reference<class std::vector<float,class std::allocator<float> > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::vector<float,class std::allocator<float> > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::vector<float,class std::allocator<float> > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(class std::vector<float,class std::allocator<float> > {lvalue},class boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(class std::vector<float,class std::allocator<float> > {lvalue},class boost::python::api::object)
        """
class ShapeInput(Boost.Python.instance):
    @staticmethod
    def __init__(*args, **kwargs):
        """
        Raises an exception
        This class cannot be instantiated from Python
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @property
    def alpha_vector(*args, **kwargs):
        ...
    @alpha_vector.setter
    def alpha_vector(*args, **kwargs):
        ...
    @property
    def atom_type_vector(*args, **kwargs):
        ...
    @atom_type_vector.setter
    def atom_type_vector(*args, **kwargs):
        ...
    @property
    def coord(*args, **kwargs):
        ...
    @coord.setter
    def coord(*args, **kwargs):
        ...
    @property
    def shift(*args, **kwargs):
        ...
    @shift.setter
    def shift(*args, **kwargs):
        ...
    @property
    def sof(*args, **kwargs):
        ...
    @sof.setter
    def sof(*args, **kwargs):
        ...
    @property
    def sov(*args, **kwargs):
        ...
    @sov.setter
    def sov(*args, **kwargs):
        ...
    @property
    def volumeAtomIndexVector(*args, **kwargs):
        ...
    @volumeAtomIndexVector.setter
    def volumeAtomIndexVector(*args, **kwargs):
        ...
@typing.overload
def AlignMol(ref: Mol, probe: Mol, refConfId: int = -1, probeConfId: int = -1, useColors: bool = True, opt_param: float = 0.5, max_preiters: int = 3, max_postiters: int = 16) -> tuple:
    """
        aligns probe to ref, probe is modified
    
        C++ signature :
            class boost::python::tuple AlignMol(class RDKit::ROMol,class RDKit::ROMol {lvalue} [,int=-1 [,int=-1 [,bool=True [,double=0.5 [,unsigned int=3 [,unsigned int=16]]]]]])
    """
@typing.overload
def AlignMol(refShape: ShapeInput, probe: Mol, probeConfId: int = -1, useColors: bool = True, opt_param: float = 0.5, max_preiters: int = 3, max_postiters: int = 16) -> tuple:
    """
        aligns probe to reference shape, probe is modified
    
        C++ signature :
            class boost::python::tuple AlignMol(struct ShapeInput,class RDKit::ROMol {lvalue} [,int=-1 [,bool=True [,double=0.5 [,unsigned int=3 [,unsigned int=16]]]]])
    """
def PrepareConformer(mol: Mol, confId: int = -1, useColors: bool = True) -> ShapeInput:
    """
        returns a shape object for a molecule
    
        C++ signature :
            struct ShapeInput * __ptr64 PrepareConformer(class RDKit::ROMol [,int=-1 [,bool=True]])
    """
