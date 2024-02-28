from __future__ import annotations

from abc import ABC
from copy import deepcopy

from gsdl.operation import IOperation
from gsdl.parameter import IParam


class AbstractOperation(IOperation, ABC):
    _params: list[IParam]
    _inputs: list[AbstractOperation]
    _is_terminal: bool
    _is_base_case: bool

    _parent_op: AbstractOperation | None
    _parent_op_idx: int | None

    def __init__(
        self,
        params: list[IParam] = None,
        inputs: list[IOperation] = None,
        is_terminal: bool = False,
        is_base_case: bool = False,
    ):
        if params is None:
            params = []
        if inputs is None:
            inputs = []
        for idx, input_op in enumerate(inputs):
            input_op._parent_op = self
            input_op._parent_op_idx = idx
        self._params = list(params)
        self._inputs = list(inputs)
        self._is_terminal = is_terminal
        self._is_base_case = is_base_case
        self._parent_op = None
        self._parent_op_idx = None

    def __add__(self, other: AbstractOperation):
        a = deepcopy(self)
        b = deepcopy(other)

        from gsdl.operation import Concat

        return Concat(a, b)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def get_params(self) -> list[IParam]:
        return list(self._params)

    def get_inputs(self) -> list[IOperation]:
        return list(self._inputs)

    def get_param_values(self) -> dict:
        result = {}

        for param in self._params:
            # TODO: Should I disallow non-param instances?
            if isinstance(param, IParam):
                result[param.get_name()] = param.get_value()

        return result

    def __str__(self):
        result = self.single_op_str()

        return result

    def __params_str(self) -> str:
        return ", ".join([str(p) for p in self._params])

    def __inputs_str(self) -> str:
        return ", ".join([str(o) for o in self._inputs])

    def single_op_str(self) -> str:
        class_name = type(self).__name__
        params = self.__params_str()
        inputs = self.__inputs_str()

        result = f"{class_name}([{params}], [{inputs}])"

        return result

    def is_implementation(self) -> bool:
        for input_op in self._inputs:
            if not input_op.is_implementation():
                return False

        return self._is_terminal_or_base_case()

    def is_terminal(self) -> bool:
        return self._is_terminal

    def is_base_case(self) -> bool:
        return self._is_base_case

    def _is_terminal_or_base_case(self) -> bool:
        return self.is_terminal() or self.is_base_case()

    def get_first_non_terminal(self) -> IOperation | None:
        for input_op in self._inputs:
            candidate = input_op.get_first_non_terminal()
            if candidate:
                return candidate

        if not self._is_terminal_or_base_case():
            return self

        return None

    def expand_operation(self, operation: IOperation) -> None:
        from gsdl.operation import Wrap

        expanded_op = Wrap(operation)

        expanded_op._parent_op = self._parent_op
        expanded_op._parent_op_idx = self._parent_op_idx

        if self._parent_op:
            idx = self._parent_op_idx
            self._parent_op._inputs[idx] = expanded_op

    def to_code(self) -> str:
        raise Exception("This operation cannot be converted to code")
