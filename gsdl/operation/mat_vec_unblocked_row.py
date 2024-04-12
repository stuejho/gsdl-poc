from gsdl.operation import AbstractOperation
from gsdl.parameter import IntParam


class MatVecUnblockedRow(AbstractOperation):
    CONST_ROW_START_NAME = "const_row_start"
    CONST_ROW_STOP_NAME = "const_row_stop"
    CONST_COL_START_NAME = "const_col_start"
    CONST_COL_STOP_NAME = "const_col_stop"

    def __init__(
        self,
        row_start: IntParam | int,
        row_stop: IntParam | int,
        col_start: IntParam | int,
        col_end: IntParam | int,
    ):
        if isinstance(row_start, int):
            r_start = IntParam(self.CONST_ROW_START_NAME).set_value(row_start)
        else:
            r_start = row_start
        if isinstance(row_stop, int):
            r_end = IntParam(self.CONST_ROW_STOP_NAME).set_value(row_stop)
        else:
            r_end = row_stop

        if isinstance(col_start, int):
            c_start = IntParam(self.CONST_ROW_START_NAME).set_value(col_start)
        else:
            c_start = col_start
        if isinstance(col_end, int):
            c_end = IntParam(self.CONST_ROW_STOP_NAME).set_value(col_end)
        else:
            c_end = col_end

        super().__init__([r_start, r_end, c_start, c_end], is_terminal=True)

    def to_code(self) -> str:
        row_start = self._params[0].get_value()
        row_stop = self._params[1].get_value()
        col_start = self._params[2].get_value()
        col_end = self._params[3].get_value()
        code = f"""
for (int row = {row_start}; row < {row_stop}; row++) {{
    for (int col = {col_start}; col < {col_end}; col++) {{
        y[row] = A[row * num_cols + col * 1] * x[col];  
    }}
}}
"""
        return code
