import textwrap

from gsdl.operation import AbstractOperation, MatVec
from gsdl.parameter import IntParam


class MatVecBlockedRow(AbstractOperation):
    CONST_ROWS_NAME = "const_rows"
    CONST_COLS_NAME = "const_cols"
    CONST_ROWS_BLOCKED_NAME = "const_cols_blocked"

    CTR = 0

    def __init__(
        self,
        num_rows: IntParam | int,
        num_cols: IntParam | int,
        num_rows_block: IntParam | int,
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
        if isinstance(num_rows_block, int):
            m_b = IntParam(self.CONST_ROWS_BLOCKED_NAME).set_value(num_rows_block)
        else:
            m_b = num_rows_block
        super().__init__([m, n, m_b], [mat_vec], is_terminal=True)

    def to_code(self, ii_start=0, jj_start=0) -> str:
        num_rows = self._params[0].get_value()
        num_cols = self._params[1].get_value()
        num_rows_block = self._params[2].get_value()
        mat_vec = self._inputs[0]
        ii = f"ii_{MatVecBlockedRow.CTR}"
        MatVecBlockedRow.CTR += 1
        code = f"""
for (int {ii} = {ii_start}; {ii} < {ii_start} + {num_rows}; {ii} += {num_rows_block}) {{
{textwrap.indent(mat_vec.to_code(ii, jj_start), "    " * 1)}
}}
"""
        return code.strip()
