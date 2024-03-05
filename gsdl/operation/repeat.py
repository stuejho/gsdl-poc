from copy import deepcopy

from gsdl.operation import AbstractOperation
from gsdl.parameter.int_param import IntParam


class Repeat(AbstractOperation):

    CONST_NAME = "const"
    PARAM_NAME = "m"

    def __init__(self, times: IntParam | int, is_base_case: bool = False):
        super().__init__([times], is_base_case=is_base_case)
