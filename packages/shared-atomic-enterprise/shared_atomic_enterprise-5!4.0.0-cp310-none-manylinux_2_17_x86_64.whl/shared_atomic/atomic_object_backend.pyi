from _typeshed import Incomplete
from typing import Any, ClassVar, Iterable

__pyx_capi__: dict
__test__: dict
cpu_count: int

class array2d:
    buf: Incomplete
    def __init__(self, x: int, y: int, itemsize: int, signed: bool = ..., iterable: Iterable = ...) -> Any:
        """__init__(self, x: int, y: int, itemsize: int, signed: bool = True, iterable: Iterable = None)

        transform of unsigned integer to signed integer,

                :param x: first dimension
                :param y: second dimension
                :param itemsize: size of each integer element
                :param signed: whether the integer element is signed
                :param iterable: initializing value in Iterable object
                :return: array2d object
        """
    def __reduce__(self):
        """__reduce_cython__(self)"""

class atomic_object:
    __pyx_vtable__: ClassVar[PyCapsule] = ...
    size: Incomplete
    def __init__(self, *args, **kwargs) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
    def __reduce__(self):
        """__reduce_cython__(self)"""

def __reduce_cython__(self) -> Any:
    """__reduce_cython__(self)"""
def __setstate_cython__(self, __pyx_state) -> Any:
    """__setstate_cython__(self, __pyx_state)"""
def atomic_object_remove(name: bytes) -> int:
    """atomic_object_remove(name: bytes) -> int

    deallocate the atomic_object except the shared_dict, which is based on file name.

         :param a: name of the atomic_object
         :return: 1 is successful
    """
