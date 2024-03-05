from __future__ import annotations

from copy import deepcopy
from typing import Callable, Self

from gsdl.parameter import AbstractParam, Operator


class IntParam(AbstractParam):
    math_operations: list[tuple[Operator, IntParam | int]] = []

    def __add__(self, other: IntParam | int) -> IntParam:
        cp = deepcopy(self)
        cp.math_operations.append((Operator.ADD, other))
        return cp

    def __sub__(self, other: IntParam | int) -> IntParam:
        cp = deepcopy(self)
        cp.math_operations.append((Operator.SUBTRACT, other))
        return cp

    def __mul__(self, other: IntParam | int) -> IntParam:
        cp = deepcopy(self)
        cp.math_operations.append((Operator.MULTIPLY, other))
        return cp

    def __gt__(self, other: IntParam | int) -> bool:
        return int(self) > int(other)

    def __int__(self):
        if self.value is None:
            raise RuntimeError("Value has not been set")
        result = self.value
        for operator, other in self.math_operations:
            result = self.__apply(operator, other)
        return result

    def __apply(self, operator: Operator, other: IntParam | int):
        match operator:
            case operator.ADD:
                return self.value + other
            case operator.SUBTRACT:
                return self.value - other
            case operator.MULTIPLY:
                return self.value * other
            case _:
                raise NotImplementedError(f"Operator {operator} not implemented")

    def __deepcopy__(self, memo):
        result = IntParam(self.name)
        result.math_operations = deepcopy(self.math_operations)
        return result

    def get_value(self):
        if self.value is None:
            return None
        return int(self)

    def __name_with_operations(self):
        if len(self.math_operations) == 0:
            return self.get_name()
        result = f"{self.get_name()}"
        for operator, other in self.math_operations:
            result = f"({result} {operator} {other})"
        return result

    def __str__(self):
        if self.value is None:
            return f"{self.__name_with_operations()}"
        return f"{self.__name_with_operations()}={self.get_value()}"

    def make_copy(self, name: str) -> Self:
        cp = deepcopy(self)
        cp.name = name
        return cp