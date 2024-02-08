import pytest

from gsdl.model import DenseMatrix, Composition


def test_valid_composition():
    mat_a = DenseMatrix(2, 1, 1, 1, "A")
    mat_b = DenseMatrix(2, 1, 1, 1, "B")
    c = Composition(mat_a, mat_b)
    assert c is not None


def test_invalid_composition():
    mat_a = DenseMatrix(2, 1, 1, 1, "A")
    mat_b = DenseMatrix(1, 1, 1, 1, "B")

    with pytest.raises(Exception) as _:
        c = Composition(mat_a, mat_b)
