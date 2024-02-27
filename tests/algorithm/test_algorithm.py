import pytest

from gsdl.algorithm import Algorithm
from gsdl.operation import AbstractOperation, IOperation
from gsdl.rule import RuleSet, Rule


class MockNonTerminalA(AbstractOperation):
    pass


class MockNonTerminalB(AbstractOperation):
    pass


class MockNonTerminalC(AbstractOperation):
    pass


class MockTerminal(AbstractOperation):
    def __init__(self):
        super().__init__(is_terminal=True)


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
            "((MockTerminal([], [])))",
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
            "(((MockTerminal([], [])) + (MockTerminal([], []))))",
        ),
    ],
)
def test_to_algorithm(operation: IOperation, rule_set: RuleSet, expected: str):
    algorithm = Algorithm(operation, rule_set)

    assert str(algorithm.to_algorithm()) == expected


@pytest.mark.parametrize(
    "operation,rule_set,expected",
    [(MockNonTerminalA(), RuleSet([Rule(MockNonTerminalA(), MockTerminal())]), "TODO")],
)
def test_to_code(operation: IOperation, rule_set: RuleSet, expected: str):
    algorithm = Algorithm(operation, rule_set)

    assert algorithm.to_code() == expected
