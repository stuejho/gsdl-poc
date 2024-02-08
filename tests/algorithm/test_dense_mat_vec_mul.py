import pytest

from gsdl.algorithm import DenseMatVecMul
from gsdl.model import DenseMatrix


@pytest.mark.parametrize(
    "func_name,mat,x,y,expected",
    [
        ("", "", "", "", "(float *, float *, float *)"),
        ("mat_vec_mul", "A", "x", "y", "mat_vec_mul(float *A, float *x, float *y)"),
    ],
)
def test_header(func_name: str, mat: str, x: str, y: str, expected: str) -> None:
    assert DenseMatVecMul.header(func_name, mat, x, y) == expected


@pytest.mark.parametrize(
    "mat,x,y,expected",
    [
        (
            DenseMatrix(1, 1, 1, 1, "M"),
            "a",
            "b",
            """
{
    for (int i = 0; i < 1; i++)
    {
        for (int j = 0; j < 1; j++)
        {
            b[j] += M[i * 1 + j * 1] * a[i];
        }
    }
}
""",
        ),
    ],
)
def test_code(mat: DenseMatrix, x: str, y: str, expected: str) -> None:
    assert DenseMatVecMul.code(mat, x, y) == expected


@pytest.mark.parametrize(
    "func_name,mat,x,y,expected",
    [
        ("", "", "", "", "(, , );"),
        ("mat_vec_mul", "X", "a", "b", "mat_vec_mul(X, a, b);"),
    ],
)
def test_call(func_name: str, mat: str, x: str, y: str, expected: str) -> None:
    assert DenseMatVecMul.call(func_name, mat, x, y) == expected
