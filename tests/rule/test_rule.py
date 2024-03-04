from unittest.mock import Mock, patch

import pytest

from gsdl.condition import ICondition
from gsdl.operation import IOperation
from gsdl.parameter import IntParam, Param
from gsdl.rule import Rule


@pytest.fixture
@patch.multiple(IOperation, __abstractmethods__=set())
def lhs() -> IOperation:
    mock = Mock(spec=IOperation)
    mock.get_params = Mock(return_value=[Param("x")])
    mock.get_inputs = Mock(return_value=[])
    mock.__str__ = Mock(return_value="lhs")
    return mock


@pytest.fixture
@patch.multiple(IOperation, __abstractmethods__=set())
def rhs() -> IOperation:
    mock = Mock(spec=IOperation)
    mock.get_params = Mock(return_value=[Param("x")])
    mock.get_inputs = Mock(return_value=[])
    mock.__str__ = Mock(return_value="rhs")
    return mock


@pytest.fixture
@patch.multiple(ICondition, __abstractmethods__=set())
def condition() -> ICondition:
    mock = Mock(ICondition())
    mock.get_params = Mock(return_value=[])
    mock.__str__ = Mock(return_value="condition")
    return mock


@pytest.fixture
def rule(lhs: IOperation, rhs: IOperation, condition: ICondition) -> Rule:
    return Rule(lhs, rhs, condition)


def test_get_lhs_returns_lhs(
    lhs: IOperation, rhs: IOperation, condition: ICondition
) -> None:
    rule = Rule(lhs, rhs, condition)

    assert rule.get_lhs() == lhs


def test_get_rhs_returns_rhs(
    lhs: IOperation, rhs: IOperation, condition: ICondition
) -> None:
    rule = Rule(lhs, rhs, condition)

    assert rule.get_rhs() == rhs


def test_get_condition_returns_condition(
    lhs: IOperation, rhs: IOperation, condition: ICondition
) -> None:
    rule = Rule(lhs, rhs, condition)

    assert rule.get_condition() == condition


def test_set_param_values_with_param_values_updates_param_values(
    lhs: IOperation, rhs: IOperation, condition: ICondition
) -> None:
    rule = Rule(lhs, rhs, condition)

    rule._params = [
        IntParam("m"),
        IntParam("m") + 1,
        IntParam("m") - 1,
    ]

    set_params = rule.set_param_values({"m": 0})
    for p in set_params:
        assert p.get_value() is not None


def test_set_param_values_without_param_values_does_not_update_param_values(
    lhs: IOperation, rhs: IOperation, condition: ICondition
) -> None:
    rule = Rule(lhs, rhs, condition)

    rule._params = [
        IntParam("m"),
        IntParam("m") + 1,
        IntParam("m") - 1,
    ]

    set_params = rule.set_param_values({})
    for p in set_params:
        try:
            v = p.get_value()
        except RuntimeError:
            v = None
        assert v is None


def test_can_evaluate_with_param_values_params_returns_true(
    lhs: IOperation, rhs: IOperation
) -> None:
    rule = Rule(lhs, rhs, None)

    rule._params = [
        IntParam("m"),
        IntParam("n"),
    ]
    param_values = {"m": 0, "n": 0}

    assert rule.can_evaluate(param_values) is True


def test_can_evaluate_without_param_values_returns_false(
    lhs: IOperation, rhs: IOperation
) -> None:
    rule = Rule(lhs, rhs, None)

    rule._params = [
        IntParam("m"),
        IntParam("m") + 1,
        IntParam("m") - 1,
    ]
    param_values = {}

    assert rule.can_evaluate(param_values) is False


def test_str_no_condition_returns_lhs_rhs(lhs: IOperation, rhs: IOperation) -> None:
    rule = Rule(lhs, rhs, None)
    expected_str = "lhs => rhs"

    assert str(rule) == expected_str


def test_str_with_condition_returns_lhs_rhs_condition(
    lhs: IOperation, rhs: IOperation, condition: ICondition
) -> None:
    rule = Rule(lhs, rhs, condition)
    expected_str = "lhs => rhs if condition"

    assert str(rule) == expected_str
