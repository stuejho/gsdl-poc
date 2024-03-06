import pytest

from gsdl.condition import GreaterThan
from gsdl.operation import IOperation
from gsdl.parameter import IntParam
from gsdl.rule import RuleSet, Rule
from tests.operation.mocks import MockRepeat, MockTerminal


def test_constructor() -> None:
    rule_set = RuleSet([])
    assert rule_set is not None


def test_rules_returns_copy() -> None:
    input_rules = []
    rule_set = RuleSet(input_rules)

    result_rules = rule_set.rules()

    assert input_rules is not result_rules


@pytest.mark.parametrize(
    "input_rules,lhs_op_to_match,expected_rule_str",
    [
        (
            [
                Rule(
                    MockRepeat(IntParam("m")),
                    MockRepeat(IntParam("m") - 1) + MockRepeat(1),
                    condition=GreaterThan(IntParam("m"), 1),
                ),
                Rule(
                    MockRepeat(1, is_base_case=True),
                    MockTerminal(),
                ),
            ],
            MockRepeat(3),
            "MockRepeat([m=3], []) => Concat(MockRepeat([(m - 1)=2], []), MockRepeat([const=1], [])) if m=3 > 1",
        ),
    ],
)
def test_get_matching_rule(
    input_rules: list[Rule], lhs_op_to_match: IOperation, expected_rule_str: str
) -> None:
    rule_set = RuleSet(input_rules)
    matching_rule = rule_set.get_matching_rule(lhs_op_to_match)

    assert str(matching_rule) == expected_rule_str
