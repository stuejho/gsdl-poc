from .i_algorithm import IAlgorithm
from gsdl.model.dense_matrix import DenseMatrix
from gsdl.util import TextUtil


class DenseMatVecMul(IAlgorithm):
    @staticmethod
    def header(func_name: str, mat: str, x: str, y: str):
        return f"{func_name}(float *{mat}, float *{x}, float *{y})"

    @staticmethod
    def code(mat: DenseMatrix, x: str, y: str):
        c = TextUtil.dedent(
            f"""
                {{
                    for (int i = 0; i < {mat.num_rows}; i++)
                    {{
                        for (int j = 0; j < {mat.num_cols}; j++)
                        {{
                            {y}[j] += {mat.ptr_name}[i * {mat.row_stride} + j * {mat.col_stride}] * {x}[i];
                        }}
                    }}
                }}
                """
        )
        return c

    @staticmethod
    def call(func_name: str, mat: str, x: str, y: str):
        return f"{func_name}({mat}, {x}, {y});"
