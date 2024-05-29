import textwrap

from gsdl.operation import AbstractOperation, MatVec
from gsdl.parameter import IntParam


class MatVecBlockedAll(AbstractOperation):
    CONST_ROWS_NAME = "const_rows"
    CONST_COLS_NAME = "const_cols"

    CTR = 0

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
            n = IntParam(self.CONST_ROWS_NAME).set_value(num_cols)
        else:
            n = num_cols
        if isinstance(num_rows_block, int):
            m_b = IntParam(self.CONST_ROWS_NAME).set_value(num_rows_block)
        else:
            m_b = num_rows_block
        if isinstance(num_cols_block, int):
            n_b = IntParam(self.CONST_COLS_NAME).set_value(num_cols_block)
        else:
            n_b = num_cols_block
        super().__init__([m, n, m_b, n_b], [mat_vec], is_terminal=True)

    def to_code(self, ii_start=0, jj_start=0) -> str:
        num_rows = self._params[0].get_value()
        num_cols = self._params[1].get_value()
        num_rows_block = self._params[2].get_value()
        num_cols_block = self._params[3].get_value()
        mat_vec = self._inputs[0]
        ii = f"ii_{MatVecBlockedAll.CTR}"
        jj = f"jj_{MatVecBlockedAll.CTR}"
        MatVecBlockedAll.CTR += 1
        code = f"""
for (int {ii} = {ii_start}; {ii} < {ii_start} + {num_rows}; {ii} += {num_rows_block}) {{
    for (int {jj} = {jj_start}; {jj} < {jj_start} + {num_cols}; {jj} += {num_cols_block}) {{
{textwrap.indent(mat_vec.to_code(ii, jj), "    " * 2)}
    }}
}}
"""
        return code.strip()
