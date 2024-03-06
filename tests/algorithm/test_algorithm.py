import pytest

from gsdl.algorithm import Algorithm
from gsdl.condition import GreaterThan
from gsdl.operation import IOperation
from gsdl.parameter import IntParam
from gsdl.rule import RuleSet, Rule
from tests.operation.mocks import (
    MockNonTerminalA,
    MockTerminal,
    MockNonTerminalB,
    MockNonTerminalC,
    MockRepeat,
)


def test_constructor():
    op = MockNonTerminalA()
    rule_set = RuleSet([Rule(MockNonTerminalA(), MockTerminal())])

    algorithm = Algorithm(op, rule_set)

    assert algorithm is not None


@pytest.mark.parametrize(
    "operation,rule_set,expected",
    [
        (
            MockNonTerminalA(),
            RuleSet([Rule(MockNonTerminalA(), MockTerminal())]),
            "(MockTerminal([], []))",
        ),
        (
            MockNonTerminalA(),
            RuleSet(
                [
                    Rule(MockNonTerminalA(), MockNonTerminalB() + MockNonTerminalC()),
                    Rule(MockNonTerminalB(), MockTerminal()),
                    Rule(MockNonTerminalC(), MockTerminal()),
                ]
            ),
            "(Concat(MockTerminal([], []), MockTerminal([], [])))",
        ),
        (
            MockRepeat(IntParam("m").set_value(3)),
            RuleSet(
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
                ]
            ),
            "(Concat(Concat(MockTerminal([], []), MockTerminal([], [])), MockTerminal([], [])))",
        ),
    ],
)
def test_to_algorithm(operation: IOperation, rule_set: RuleSet, expected: str):
    algorithm = Algorithm(operation, rule_set)

    assert str(algorithm.to_algorithm()) == expected


@pytest.mark.parametrize(
    "operation,rule_set,expected",
    [
        (MockNonTerminalA(), RuleSet([Rule(MockNonTerminalA(), MockTerminal())]), "a"),
        (
            MockRepeat(IntParam("m").set_value(3)),
            RuleSet(
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
                ]
            ),
            "aaa",
        ),
    ],
)
def test_to_code(operation: IOperation, rule_set: RuleSet, expected: str):
    algorithm = Algorithm(operation, rule_set)

    assert algorithm.to_code() == expected
