from gsdl.condition import AbstractCondition
from gsdl.parameter import IntParam


class GreaterThan(AbstractCondition):
    lhs: IntParam | int
    rhs: IntParam | int

    def __init__(self, lhs: IntParam | int, rhs: IntParam | int):
        super().__init__([lhs, rhs], lambda a, b: a > b)

        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f"{self.lhs} > {self.rhs}"
