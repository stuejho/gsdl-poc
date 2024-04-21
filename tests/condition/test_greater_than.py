from gsdl.condition import GreaterThan
from gsdl.parameter import IntParam


def test_str_returns_expected_str() -> None:
    a = IntParam("a")
    a.set_value(1)

    b = IntParam("b")
    b.set_value(2)

    gt = GreaterThan(a, b)

    assert str(gt) == "a=1 > b=2"


def test_get_params_returns_constructor_params() -> None:
    a = IntParam("a")
    a.set_value(1)

    b = IntParam("b")
    b.set_value(2)

    gt = GreaterThan(a, b)

    params = gt.get_params()
    assert params[0] == a
    assert params[1] == b


def test_is_match_lhs_greater_than_rhs_evaluates_true() -> None:
    a = IntParam("a")
    a.set_value(2)

    b = IntParam("b")
    b.set_value(1)

    gt = GreaterThan(a, b)

    assert gt.evaluate() is True


def test_is_match_lhs_not_greater_than_rhs_evaluates_false() -> None:
    a = IntParam("a")
    a.set_value(1)

    b = IntParam("b")
    b.set_value(2)

    gt = GreaterThan(a, b)

    assert gt.evaluate() is False
