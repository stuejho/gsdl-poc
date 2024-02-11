from gsdl.model import DenseMatrix


def test_valid_dense_matrix():
    mat = DenseMatrix(5, 5, 1, 1, "M")
    assert mat is not None
