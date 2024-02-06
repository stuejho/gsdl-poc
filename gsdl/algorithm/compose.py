from .i_algorithm import IAlgorithm
from .dense_mat_vec_mul import DenseMatVecMul
from gsdl.model import Composition
from gsdl.util import TextUtil


class Compose(IAlgorithm):
    @staticmethod
    def header(func_name: str, mat_a: str, mat_b: str, x: str, y: str):
        return f"{func_name}(float *{mat_a}, float *{mat_b}, float *{x}, float *{y})"

    @staticmethod
    def code(composition: Composition, x: str, y: str) -> str:
        compose_1 = DenseMatVecMul.code(composition.B, x, "z")
        compose_2 = DenseMatVecMul.code(composition.A, "z", y)
        c = TextUtil.dedent(
            f"""
            {{
                float z[{composition.B.num_rows}];
                {TextUtil.indent_by_level(compose_1, 4)}
                {TextUtil.indent_by_level(compose_2, 4)}
            }}
            """
        )
        return c

    @staticmethod
    def call(func_name: str, mat_a: str, mat_b: str, x: str, y: str):
        return f"{func_name}({mat_a}, {mat_b}, {x}, {y});"
