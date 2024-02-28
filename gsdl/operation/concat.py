from gsdl.common import IImplementation
from gsdl.operation import AbstractOperation, IOperation


class Concat(AbstractOperation, IImplementation):
    def __init__(self, op_a: IOperation, op_b: IOperation):
        super().__init__([], [op_a, op_b], is_base_case=True)

    def single_op_str(self):
        op_a = self._inputs[0]
        op_b = self._inputs[1]
        return f"Concat({op_a}, {op_b})"

    def to_code(self) -> str:
        op_a = self._inputs[0]
        op_b = self._inputs[1]
        if isinstance(op_a, IImplementation) and isinstance(op_b, IImplementation):
            return op_a.to_code() + op_b.to_code()
        raise Exception("Not all operations can be converted to code implementations")
