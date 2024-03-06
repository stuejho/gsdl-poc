from abc import ABC
from copy import deepcopy

from gsdl.parameter import IParam


class AbstractParam(IParam, ABC):
    name: str
    value: any

    def __init__(self, name: str):
        self.name = name
        self.value = None

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def set_value(self, value: any):
        self.value = value
        return self

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
