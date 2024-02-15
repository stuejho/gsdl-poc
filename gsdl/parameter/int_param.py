from __future__ import annotations

from copy import deepcopy
from typing import Callable

from gsdl.parameter import AbstractParam


class IntParam(AbstractParam):
    math_operations: list[Callable[[IntParam | int], int]] = []

    def __add__(self, other: IntParam | int) -> IntParam:
        cp = deepcopy(self)
        cp.math_operations.append(lambda x: x + other)
        return cp

    def __sub__(self, other: IntParam | int) -> IntParam:
        cp = deepcopy(self)
        cp.math_operations.append(lambda x: x - other)
        return cp

    def __mul__(self, other: IntParam | int) -> IntParam:
        cp = deepcopy(self)
        cp.math_operations.append(lambda x: x * other)
        return cp

    def __gt__(self, other: IntParam | int) -> bool:
        return int(self) > int(other)

    def __int__(self):
        if self.value is None:
            raise Exception("Value has not been set")
        result = self.value
        for operation in self.math_operations:
            result = operation(result)
        return result

    def __deepcopy__(self, memo):
        result = IntParam(self.name)
        result.math_operations = deepcopy(self.math_operations)
        return result

    def get_value(self):
        return int(self)
