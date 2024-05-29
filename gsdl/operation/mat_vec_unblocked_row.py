from gsdl.operation import AbstractOperation
from gsdl.parameter import IntParam


class MatVecUnblockedRow(AbstractOperation):
    CONST_ROW_STOP_NAME = "const_row_stop"
    CONST_COL_STOP_NAME = "const_col_stop"

    def __init__(
        self,
        row_stop: IntParam | int,
        col_end: IntParam | int,
    ):
        if isinstance(row_stop, int):
            r_end = IntParam(self.CONST_ROW_STOP_NAME).set_value(row_stop)
        else:
            r_end = row_stop

        if isinstance(col_end, int):
            c_end = IntParam(self.CONST_ROW_STOP_NAME).set_value(col_end)
        else:
            c_end = col_end

        super().__init__([r_end, c_end], is_terminal=True)

    def to_code(self, row_start: str | int = 0, col_start: str | int = 0) -> str:
        row_stop = self._params[0].get_value()
        col_stop = self._params[1].get_value()
        code = f"""
for (int i = {row_start}; i < {row_start} + {row_stop}; i++) {{
    for (int j = {col_start}; j < {col_start} + {col_stop}; j++) {{
        y[i] += A[i * N + j * 1] * x[j]; 
    }}
}}
"""
        return code.strip()
