import pytest

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
        (Param("m"), 0, "0"),
        (Param("hello"), 1, "1"),
    ],
)
def test_str_returns_string(param: Param, set_value: any, expected_value: str) -> None:
    param.set_value(set_value)
    assert str(param) == expected_value
