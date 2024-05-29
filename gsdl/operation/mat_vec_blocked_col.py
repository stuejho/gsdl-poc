import textwrap

from gsdl.operation import AbstractOperation, MatVec
from gsdl.parameter import IntParam


class MatVecBlockedCol(AbstractOperation):
    CONST_ROWS_NAME = "const_rows"
    CONST_COLS_NAME = "const_cols"
    CONST_COLS_BLOCK_NAME = "const_cols_block"

    CTR = 0

    def __init__(
        self,
        num_rows: IntParam | int,
        num_cols: IntParam | int,
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
        if isinstance(num_cols_block, int):
            n_b = IntParam(self.CONST_COLS_BLOCK_NAME).set_value(num_cols_block)
        else:
            n_b = num_cols_block
        super().__init__([m, n, n_b], [mat_vec], is_terminal=True)

    def to_code(self, ii_start=0, jj_start=0) -> str:
        num_rows = self._params[0].get_value()
        num_cols = self._params[1].get_value()
        num_cols_block = self._params[2].get_value()
        mat_vec = self._inputs[0]
        jj = f"jj_{MatVecBlockedCol.CTR}"
        MatVecBlockedCol.CTR += 1
        code = f"""
for (int {jj} = {jj_start}; {jj} < {jj_start} + {num_cols}; {jj} += {num_cols_block}) {{
{textwrap.indent(mat_vec.to_code(ii_start, jj), "    " * 1)}
}}
"""
        return code.strip()
