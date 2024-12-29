# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from inspect import isabstract
from typing import Type, Dict, List

try:
    from typing import Self

except ImportError:
    # For earlier versions...
    from typing_extensions import Self


class IFactory(ABC):
    """ Base interface for classes that acts like factories """

    _impls: Dict[str, Type[Self]] = {}

    def __init_subclass__(cls):
        if not isabstract(cls):
            cls._impls[cls.registered_name()] = cls

    @classmethod
    def impls(cls) -> List[str]:
        """ It returns the current implementations """
        return [k for k in cls._impls.keys()]

    @classmethod
    @abstractmethod
    def registered_name(cls) -> str:
        """ It returns the name to use when the class is registered """

    @classmethod
    def get_implementation(cls, registered_name: str) -> Type[Self]:
        """ It returns the implementation class by the registered name """
        return cls._impls.get(registered_name, None)
