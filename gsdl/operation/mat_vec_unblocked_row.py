from gsdl.operation import AbstractOperation
from gsdl.parameter import IntParam


class MatVecUnblockedRow(AbstractOperation):
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
        super().__init__([m, n], is_terminal=True)

    def to_code(self) -> str:
        num_rows = self._params[0].get_value()
        num_cols = self._params[1].get_value()
        code = f"""
for (int row = 0; row < {num_rows}; row++) {{
    for (int col = 0; col < {num_cols}; col++) {{
        y[row] = A[row * num_cols + col * 1] * x[col];  
    }}
}}
"""
        return code
