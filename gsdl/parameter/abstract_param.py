from abc import ABC
from copy import deepcopy
from typing import Self

from gsdl.parameter import IParam


class AbstractParam(IParam, ABC):
    name: str
    value: any
    params: list[IParam]

    def __init__(self, name: str):
        self.name = name
        self.value = None
        self.params = [self]

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def set_value(self, value: any):
        self.value = value
        return self

    def get_params(self) -> list[Self]:
        return list(self.params)

    def __str__(self):
        if self.value is None:
            return f"{self.get_name()}"
        return f"{self.get_name()} = {self.get_value()}"

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __add__(self, other: any) -> IParam:
        raise NotImplementedError

    def __sub__(self, other: any) -> IParam:
        raise NotImplementedError

    def __mul__(self, other: any) -> IParam:
        raise NotImplementedError

    def __lt__(self, other: any):
        from gsdl.condition import LessThan

        return LessThan(self, other)

    def __gt__(self, other: any):
        from gsdl.condition import GreaterThan

        return GreaterThan(self, other)

    def __eq__(self, other: any):
        from gsdl.condition import EqualTo

        return EqualTo(self, other)
