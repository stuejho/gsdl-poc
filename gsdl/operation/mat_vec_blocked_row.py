from gsdl.operation import AbstractOperation, MatVec
from gsdl.parameter import IntParam


class MatVecBlockedRow(AbstractOperation):
    CONST_ROWS_NAME = "const_rows"
    CONST_COLS_NAME = "const_cols"

    def __init__(
        self,
        num_rows: IntParam | int,
        num_cols: IntParam | int,
        num_rows_block: IntParam | int,
        num_cols_block: IntParam | int,
        mat_vec: MatVec,
    ):
        if isinstance(num_rows, int):
            m = IntParam(self.CONST_ROWS_NAME).set_value(num_rows)
        else:
            m = num_rows
        if isinstance(num_cols, int):
            n = IntParam(self.CONST_COLS_NAME).set_value(num_cols)
        else:
            n = num_cols
        super().__init__([m, n, num_rows_block, num_cols_block], [mat_vec], is_terminal=True)

    def to_code(self) -> str:
        num_rows = self._params[0].get_value()
        num_cols = self._params[1].get_value()
        num_rows_block = self._params[2].get_value()
        num_cols_block = self._params[3].get_value()
        mat_vec = self._inputs[0]
        code = f"""
for (int row_block_idx = 0; row_block_idx < {num_rows}; row_block_idx++) {{
    for (int row = 0; row < {num_rows}; row++) {{
        for (int col = 0; col < {num_cols}; col++) {{
            y[row] = A[row * num_cols + col * 1] * x[col];  
        }}
    }}
}}
{mat_vec.to_code()}
"""
        return code
