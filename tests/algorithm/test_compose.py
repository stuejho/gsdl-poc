import pytest

from gsdl.algorithm import Compose
from gsdl.model import Composition, DenseMatrix


@pytest.mark.parametrize(
    "func_name,mat_a,mat_b,x,y,expected",
    [
        ("", "", "", "", "", "(float *, float *, float *, float *)"),
        (
            "compose",
            "A",
            "B",
            "x",
            "y",
            "compose(float *A, float *B, float *x, float *y)",
        ),
    ],
)
def test_header(
    func_name: str, mat_a: str, mat_b: str, x: str, y: str, expected: str
) -> None:
    assert Compose.header(func_name, mat_a, mat_b, x, y) == expected


@pytest.mark.parametrize(
    "composition,x,y,expected",
    [
        (
            Composition(DenseMatrix(1, 1, 1, 1, "M"), DenseMatrix(1, 1, 1, 1, "N")),
            "a",
            "b",
            """
{
    float z[1];

    {
        for (int i = 0; i < 1; i++)
        {
            for (int j = 0; j < 1; j++)
            {
                z[j] += N[i * 1 + j * 1] * a[i];
            }
        }
    }


    {
        for (int i = 0; i < 1; i++)
        {
            for (int j = 0; j < 1; j++)
            {
                b[j] += M[i * 1 + j * 1] * z[i];
            }
        }
    }

}
""",
        ),
    ],
)
def test_code(composition: Composition, x: str, y: str, expected: str) -> None:
    assert Compose.code(composition, x, y) == expected


@pytest.mark.parametrize(
    "func_name,mat_a,mat_b,x,y,expected",
    [
        ("", "", "", "", "", "(, , , );"),
        ("compose", "A", "B", "x", "y", "compose(A, B, x, y);"),
    ],
)
def test_call(
    func_name: str, mat_a: str, mat_b: str, x: str, y: str, expected: str
) -> None:
    assert Compose.call(func_name, mat_a, mat_b, x, y) == expected
