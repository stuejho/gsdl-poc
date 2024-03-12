import pytest

from gsdl.condition import GreaterThan, EqualTo
from gsdl.generator import IntGenerator
from gsdl.operation import IOperation
from gsdl.parameter import IntParam
from gsdl.rule import RuleSet, Rule
from gsdl.set_builder import SetBuilder
from tests.operation.mocks import MockRepeat, MockTerminal, MockTwoParamNonTerminal


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
                    MockTwoParamNonTerminal(IntParam("m"), IntParam("n")),
                    MockRepeat(50) + MockRepeat(50),
                    condition=EqualTo(IntParam("m"), 100),
                ),
                Rule(
                    MockRepeat(IntParam("m")),
                    MockRepeat(IntParam("m") - 1) + MockRepeat(1),
                    condition=GreaterThan(IntParam("m"), 1),
                ),
                Rule(
                    MockRepeat(1, is_base_case=True),
                    MockTerminal(),
                    condition=EqualTo(IntParam("m"), 1),
                ),
            ],
            MockRepeat(3),
            "MockRepeat([m=3], []) => Concat(MockRepeat([(m - 1)=2], []), MockRepeat([const=1], [])) if m=3 > 1",
        ),
    ],
)
def test_get_matching_first_rule(
    input_rules: list[Rule], lhs_op_to_match: IOperation, expected_rule_str: str
) -> None:
    rule_set = RuleSet(input_rules)
    matching_rule = rule_set.get_first_matching_rule(lhs_op_to_match)

    assert str(matching_rule) == expected_rule_str


@pytest.mark.parametrize(
    "input_rules,lhs_op_to_match,expected_num_matching_rules",
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
                    condition=EqualTo(IntParam("m"), 1),
                ),
            ],
            MockRepeat(3),
            1,
        ),
        (
            [
                Rule(
                    MockRepeat(IntParam("m")),
                    MockRepeat(50) + MockRepeat(50),
                    condition=EqualTo(IntParam("m"), 100),
                ),
                Rule(
                    MockRepeat(IntParam("m")),
                    MockRepeat(IntParam("m") - 1) + MockRepeat(1),
                    condition=GreaterThan(IntParam("m"), 1),
                ),
                Rule(
                    MockRepeat(IntParam("m")),
                    MockRepeat(IntParam("m") - 1) + MockRepeat(1),
                    condition=GreaterThan(IntParam("m"), 1),
                    parameter_set=SetBuilder(
                        (IntParam("l"), IntParam("k")),
                        (
                            (
                                IntParam("l"),
                                IntGenerator(0, (IntParam("m").set_value(5)), 1),
                            ),
                            (
                                IntParam("k"),
                                IntGenerator(0, (IntParam("m").set_value(5)), 1),
                            ),
                        ),
                        IntParam("l") + IntParam("k") == IntParam("m").set_value(5),
                    ),
                ),
                Rule(
                    MockRepeat(1, is_base_case=True),
                    MockTerminal(),
                    condition=EqualTo(IntParam("m"), 1),
                ),
            ],
            MockRepeat(3),
            2,
        ),
    ],
)
def test_get_matching_first_rule(
    input_rules: list[Rule],
    lhs_op_to_match: IOperation,
    expected_num_matching_rules: int,
) -> None:
    rule_set = RuleSet(input_rules)
    matching_rules = rule_set.get_matching_rules(lhs_op_to_match)

    assert len(matching_rules) == expected_num_matching_rules
