from gsdl.operation import AbstractOperation
from gsdl.parameter.int_param import IntParam


class Repeat(AbstractOperation):

    CONST_NAME = "const"

    def __init__(self, times: IntParam | int, is_base_case: bool = False):
        if isinstance(times, int):
            t = IntParam(self.CONST_NAME).set_value(times)
        else:
            t = times
        super().__init__([t], is_base_case=is_base_case)
