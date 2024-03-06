from gsdl.condition import EqualTo
from gsdl.parameter import IntParam


def test_str_returns_expected_str() -> None:
    a = IntParam("a")
    a.set_value(1)

    b = IntParam("b")
    b.set_value(2)

    et = EqualTo(a, b)

    assert str(et) == "a=1 == b=2"


def test_get_params_returns_constructor_params() -> None:
    a = IntParam("a")
    a.set_value(1)

    b = IntParam("b")
    b.set_value(2)

    et = EqualTo(a, b)

    params = et.get_params()
    assert params[0] == a
    assert params[1] == b


def test_is_match_lhs_equal_to_rhs_evaluates_true() -> None:
    a = IntParam("a")
    a.set_value(2)

    b = IntParam("b")
    b.set_value(2)

    et = EqualTo(a, b)

    assert et.is_match() is True


def test_is_match_lhs_not_equal_to_rhs_evaluates_false() -> None:
    a = IntParam("a")
    a.set_value(1)

    b = IntParam("b")
    b.set_value(2)

    et = EqualTo(a, b)

    assert et.is_match() is False
