from gsdl import algorithm
from gsdl.algorithm import DenseMatVecMul
from gsdl.algorithm.compose import Compose
from gsdl.model import DenseMatrix, Composition


def main():
    a_mat = DenseMatrix(5, 5, 1, 1, "A")
    mm_head = DenseMatVecMul.header("mat_vec_mul", "A", "x", "y")
    mm_code = DenseMatVecMul.code(a_mat, "x", "y")
    mm_call = DenseMatVecMul.call("mat_vec_mul", "A", "a", "b")
    print(mm_head)
    print(mm_code)

    a_mat = DenseMatrix(5, 5, 1, 1, "A")
    b_mat = DenseMatrix(5, 5, 1, 1, "B")
    comp = Composition(A=a_mat, B=b_mat)
    comp_head = Compose.header("compose", "A", "B", "x", "y")
    comp_code = Compose.code(comp, "x", "y")
    comp_call = Compose.call("compose", "A", "B", "a", "b")
    print(comp_head)
    print(comp_code)

    print(mm_call)
    print(comp_call)


if __name__ == "__main__":
    main()
