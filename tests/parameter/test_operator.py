from gsdl.parameter import Operator


def test_str():
    assert str(Operator.ADD) == "+"
    assert str(Operator.SUBTRACT) == "-"
    assert str(Operator.MULTIPLY) == "*"
