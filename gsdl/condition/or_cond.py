from gsdl.condition import AbstractCondition, ICondition


class Or(AbstractCondition):
    lhs: ICondition
    rhs: ICondition

    def __init__(self, lhs: ICondition, rhs: ICondition):
        super().__init__(lhs.get_params() + rhs.get_params(), lambda: False)

        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f"{self.lhs} and {self.rhs}"

    def evaluate(self):
        return self.lhs.evaluate() or self.rhs.evaluate()
