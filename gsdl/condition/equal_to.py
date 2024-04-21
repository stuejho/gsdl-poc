from gsdl.condition import AbstractCondition
from gsdl.parameter import IParam


class EqualTo(AbstractCondition):
    lhs: IParam | int
    rhs: IParam | int

    def __init__(self, lhs: IParam | int, rhs: IParam | int):
        super().__init__([lhs, rhs], lambda a, b: a == b)

        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f"{self.lhs} == {self.rhs}"
