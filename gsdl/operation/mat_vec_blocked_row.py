import textwrap

from gsdl.operation import AbstractOperation, MatVec
from gsdl.parameter import IntParam


class MatVecBlockedRow(AbstractOperation):
    CONST_ROWS_NAME = "const_rows"
    CONST_COLS_NAME = "const_cols"

    CTR = 0

    def __init__(
        self,
        num_rows_block: IntParam | int,
        num_cols_block: IntParam | int,
        mat_vec: MatVec,
    ):
        if isinstance(num_rows_block, int):
            m = IntParam(self.CONST_ROWS_NAME).set_value(num_rows_block)
        else:
            m = num_rows_block
        if isinstance(num_cols_block, int):
            n = IntParam(self.CONST_COLS_NAME).set_value(num_cols_block)
        else:
            n = num_cols_block
        super().__init__([m, n], [mat_vec], is_terminal=True)

    def to_code(self, ii_start=0, jj_start=0) -> str:
        num_rows_block = self._params[0].get_value()
        num_cols_block = self._params[1].get_value()
        mat_vec = self._inputs[0]
        ii = f"ii_{MatVecBlockedRow.CTR}"
        jj = f"jj_{MatVecBlockedRow.CTR}"
        MatVecBlockedRow.CTR += 1
        code = f"""
for (int {ii} = {ii_start}; {ii} < {num_rows_block}; {ii}++) {{
    for (int {jj} = {jj_start}; {jj} < {num_cols_block}; {jj}++) {{
{textwrap.indent(
            mat_vec.to_code(ii + ' * ' + str(num_rows_block), jj + ' * ' + str(num_cols_block)), 
            "    " * 2)
}
    }}
}}
"""
        return code.strip()
