from gsdl.operation import AbstractOperation
from gsdl.parameter import IntParam


class MatVec(AbstractOperation):
    CONST_ROWS_NAME = "const_rows"
    CONST_COLS_NAME = "const_cols"

    def __init__(self, num_rows: IntParam | int, num_cols: IntParam | int):
        if isinstance(num_rows, int):
            m = IntParam(self.CONST_ROWS_NAME).set_value(num_rows)
        else:
            m = num_rows
        if isinstance(num_cols, int):
            n = IntParam(self.CONST_COLS_NAME).set_value(num_cols)
        else:
            n = num_cols
        super().__init__([m, n])
