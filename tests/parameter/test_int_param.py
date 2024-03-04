import pytest

from gsdl.parameter import IntParam


@pytest.mark.parametrize(
    "int_param,expected_name",
    [
        (IntParam("m"), "m"),
        (IntParam("hello"), "hello"),
    ],
)
def test_get_name_returns_name_from_constructor(
    int_param: IntParam, expected_name: str
) -> None:
    assert int_param.get_name() == expected_name


@pytest.mark.parametrize(
    "int_param,set_value,expected_value",
    [
        (IntParam("m"), 0, 0),
        (IntParam("hello"), 1, 1),
    ],
)
def test_get_value_after_set_value_returns_value(
    int_param: IntParam, set_value: int, expected_value: int
) -> None:
    int_param.set_value(set_value)

    assert int_param.get_value() == expected_value


@pytest.mark.parametrize(
    "int_param,expected_message",
    [
        (IntParam("m"), "Value has not been set"),
        (IntParam("hello"), "Value has not been set"),
    ],
)
def test_get_value_without_set_value_throws_exception(
    int_param: IntParam, expected_message: str
) -> None:
    with pytest.raises(RuntimeError) as e_info:
        int_param.get_value()
    assert e_info.type is RuntimeError
    assert expected_message == str(e_info.value)


@pytest.mark.parametrize(
    "int_param,set_value,expected_value",
    [
        (IntParam("m"), 0, "0"),
        (IntParam("hello"), 1, "1"),
    ],
)
def test_str_returns_string(
    int_param: IntParam, set_value: int, expected_value: str
) -> None:
    int_param.set_value(set_value)
    assert str(int_param) == expected_value


@pytest.mark.parametrize(
    "int_param_a,int_param_b",
    [
        (IntParam("m"), 1),
        (IntParam("hello"), IntParam("world")),
    ],
)
def test_arithmethic_operation_returns_copy(
    int_param_a: IntParam, int_param_b: IntParam
) -> None:
    assert int_param_a is not int_param_a + int_param_b
    assert int_param_a is not int_param_a - int_param_b
    assert int_param_a is not int_param_a * int_param_b


def test_add_int_param_int_returns_int() -> None:
    a = IntParam("a")
    result = a + 1
    result.set_value(0)

    assert result.get_value() == 1


def test_sub_int_param_int_returns_int() -> None:
    a = IntParam("a")
    result = a - 1
    result.set_value(0)

    assert result.get_value() == -1


def test_mul_int_param_int_returns_int() -> None:
    a = IntParam("a")
    result = a * 5
    result.set_value(5)

    assert result.get_value() == 25


def test_gt_int_param_compared_with_smaller_value_returns_true() -> None:
    a = IntParam("a")
    a.set_value(0)

    assert (a > -1) is True


def test_gt_int_param_compared_with_smaller_value_returns_false() -> None:
    a = IntParam("a")
    a.set_value(0)

    assert (a > 1) is False
