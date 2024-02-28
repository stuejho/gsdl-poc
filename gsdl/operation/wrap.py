from gsdl.common import IImplementation
from gsdl.operation import AbstractOperation, IOperation


class Wrap(AbstractOperation, IImplementation):
    def __init__(self, operation: IOperation):
        super().__init__([], [operation], is_base_case=True)

    def single_op_str(self):
        input_op = self._inputs[0]
        return f"({input_op})"

    def to_code(self):
        return self._inputs[0].to_code()
