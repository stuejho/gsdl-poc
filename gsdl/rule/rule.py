from gsdl.condition import ICondition
from gsdl.operation import IOperation
from gsdl.parameter import IParam
from gsdl.rule import IRule


class Rule(IRule):
    _params: list[IParam] = []

    def __init__(self, lhs: IOperation, rhs: IOperation, condition: ICondition = None):
        self.lhs = lhs
        self.rhs = rhs
        self.condition = condition

        self.__post_init__()

    def __post_init__(self):
        self._params = []

        self.__add_params(self.lhs.get_params())

        self.__add_params(self.rhs.get_params())
        operations = list(self.rhs.get_inputs())
        while operations:
            op = operations.pop()
            self.__add_params(op.get_params())
            for rhs_in in op.get_inputs():
                operations.append(rhs_in)

        if self.condition is not None:
            self.__add_params(self.condition.get_params())

    def __add_params(self, params: list[IParam]):
        for param in params:
            if isinstance(param, IParam):
                self._params.append(param)

    def get_lhs(self) -> IOperation:
        return self.lhs

    def get_rhs(self) -> IOperation:
        return self.rhs

    def get_condition(self) -> ICondition:
        return self.condition

    def set_param_values(self, param_values: dict) -> list[IParam]:
        for param in self._params:
            param_name = param.get_name()
            param_value = param_values.get(param_name)
            if param_value is not None:
                param.set_value(param_value)
        return list(self._params)

    def can_evaluate(self, param_values: dict) -> bool:
        for param in self._params:
            if (param.get_name() not in param_values.keys()) and (
                param.get_value() is None
            ):
                return False
        return True

    def __str__(self):
        result = f"{self.lhs} => {self.rhs}"

        if self.condition:
            result += f" if {self.condition}"

        return result
