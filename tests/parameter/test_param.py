import pytest

from gsdl.condition import LessThan, GreaterThan, EqualTo
from gsdl.parameter import Param


@pytest.mark.parametrize(
    "param,expected_name",
    [
        (Param("m"), "m"),
        (Param("hello"), "hello"),
    ],
)
def test_get_name_returns_name_from_constructor(
    param: Param, expected_name: str
) -> None:
    assert param.get_name() == expected_name


@pytest.mark.parametrize(
    "param,set_value,expected_value",
    [
        (Param("m"), 0, 0),
        (Param("hello"), [], []),
    ],
)
def test_get_value_after_set_value_returns_value(
    param: Param, set_value: any, expected_value: any
) -> None:
    param.set_value(set_value)

    assert param.get_value() == expected_value


@pytest.mark.parametrize(
    "param,set_value,expected_value",
    [
        (Param("m"), None, "m"),
        (Param("m"), 0, "m = 0"),
        (Param("hello"), 1, "hello = 1"),
    ],
)
def test_str_returns_string(param: Param, set_value: any, expected_value: str) -> None:
    param.set_value(set_value)
    assert str(param) == expected_value


def test_add_raises_not_implemented_error() -> None:
    a = Param("a")
    b = Param("b")
    with pytest.raises(NotImplementedError):
        _ = a + b


def test_sub_returns_not_implemented_error() -> None:
    a = Param("a")
    b = Param("b")
    with pytest.raises(NotImplementedError):
        _ = a - b


def test_mul_returns_not_implemented_error() -> None:
    a = Param("a")
    b = Param("b")
    with pytest.raises(NotImplementedError):
        _ = a * b


def test_lt_returns_less_than() -> None:
    a = Param("a")
    b = Param("b")
    result = a < b
    assert isinstance(result, LessThan)


def test_gt_returns_less_than() -> None:
    a = Param("a")
    b = Param("b")
    result = a > b
    assert isinstance(result, GreaterThan)


def test_eq_returns_less_than() -> None:
    a = Param("a")
    b = Param("b")
    result = a == b
    assert isinstance(result, EqualTo)
