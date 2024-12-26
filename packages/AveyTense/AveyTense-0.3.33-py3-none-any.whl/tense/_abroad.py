"""
**Tense Nennai Types** \n
\\@since 0.3.29 \\
© 2023-Present Aveyzan // License: MIT
```ts
module tense._abroad
```
This internal module has been established to extend possibilities of `abroad()` \\
function and its variations.
"""

from . import _primal_types as _pt
from ._abc import (
    Iterable as _Iterable
)

__module__ = "tense"
_var = _pt.TypeVar

_T = _var("_T")

class _AbroadUnknownInitializer(_pt.Generic[_T]):
    """\\@since 0.3.29"""
    
    def __init__(self, seq: _Iterable[_T], v1: int, v2: int, m: int, /):
        
        self.__l = list(seq)
        self.__p = (v1, v2, m)
        
    def __iter__(self):
        
        return iter(self.__l)
    
    def __reversed__(self):
        """\\@since 0.3.32"""
        
        return reversed(self.__l)
    
    def __str__(self):
        
        if len(self.__l) == 0:
            return "abroad( <empty> )"
        
        else:
            
            if self.__p == (0, 0, 0):
                return "abroad( <mixed> )"
            
            return "abroad({})".format(", ".join([str(e) for e in self.__p]))
            
    def __repr__(self):
        
        return "<{}.{} object: {}>".format(__module__, type(self).__name__, self.__str__())
    
    def __pos__(self):
        """
        \\@since 0.3.28
        
        Returns sequence as a list. `+` can be claimed as "allow to change any items, this sequence can be updated"
        """
        return self.__l
    
    def __neg__(self):
        """
        \\@since 0.3.28
        
        Returns sequence as a tuple. `-` can be claimed as "do not change any items, this sequence cannot be updated"
        """
        return tuple(self.__l)
    
    def __invert__(self):
        """
        \\@since 0.3.28
        
        Returns sequence as a set. `~` can be claimed as "allow to change any items, this sequence can be updated, BUT items must be unique"
        """
        return set(self.__l)
    
    def __getitem__(self, key: int):
        """
        \\@since 0.3.29. `self[key]`
        """
        try:
            return self.__l[key]
        
        except IndexError:
            error = IndexError("sequence out of range")
            raise error
        
    def __contains__(self, item: _T):
        """
        \\@since 0.3.32. `item in self`
        """
        return item in self.__l
    
    def __add__(self, other: _pt.Union[_Iterable[_T], _pt.Self]):
        """
        \\@since 0.3.32. `self + other`
        """
        if not isinstance(other, (_Iterable, type(self))):
            error = TypeError("expected an iterable or abroad() function result as a right operand")
            raise error
        
        # 1st statement: obvious certificate that this class has the __iter__
        # method, so it satisfies requirement for list constructor
        if (isinstance(other, type(self)) and len(list(other)) == 0) or (isinstance(other, _Iterable) and len(other) == 0):
            return self
        
        # this notation seems ugly since there is double invocation, but
        # necessary in case of inheritance, so code will type hint subclasses
        # objects as returned results. this notation is also here due to
        # refraining from using base class as a role of constructor - type
        # hinted will be object of base class, what might not be a good idea
        return type(self)(self.__l + [e for e in other], 0, 0, 0) 
    
    def __radd__(self, other: _pt.Union[_Iterable[_T], _pt.Self]):
        """
        \\@since 0.3.32. `other + self`
        """
        if not isinstance(other, (_Iterable, type(self))):
            error = TypeError("expected an iterable or abroad() function result as a left operand")
            raise error
        
        if (isinstance(other, type(self)) and len(list(other)) == 0) or (isinstance(other, _Iterable) and len(other) == 0):
            return self
        
        return type(self)([e for e in other] + self.__l, 0, 0, 0)
    
    def __mul__(self, other: int):
        """
        \\@since 0.3.32. `self * other`
        """
        if not isinstance(other, int) or (isinstance(other, int) and other < 1):
            error = TypeError("expected a non-negative integer as a right operand")
            raise error
        
        return type(self)(self.__l * other, self.__p[0], self.__p[1], self.__p[2])
    
    def __rmul__(self, other: int):
        """
        \\@since 0.3.32. `other * self`
        """
        if not isinstance(other, int) or (isinstance(other, int) and other < 1):
            error = TypeError("expected a non-negative integer as a left operand")
            raise error
        
        return type(self)(self.__l * other, self.__p[0], self.__p[1], self.__p[2])
       
    @property
    def params(self):
        """
        \\@since 0.3.29
        
        Returns parameters as integers
        """
        return self.__p
    
    @params.getter
    def params(self):
        return self.__p
    
    @params.deleter
    def params(self):
        error = TypeError("cannot delete property 'params'")
        raise error
    
    @params.setter
    def params(self, value):
        error = TypeError("cannot set new value to property 'params'")
        raise error
    
class AbroadInitializer(_AbroadUnknownInitializer[int]): ... # since 0.3.28
class AbroadStringInitializer(_AbroadUnknownInitializer[str]): ... # since 0.3.29
class AbroadFloatyInitializer(_AbroadUnknownInitializer[float]): ... # since 0.3.29