from unittest.mock import patch, Mock

import pytest

from gsdl.operation import Wrap, IOperation, Terminal


@pytest.fixture
@patch.multiple(IOperation, __abstractmethods__=set())
def operation() -> IOperation:
    mock = Mock(spec=IOperation)
    mock.__str__ = Mock(return_value="operation")
    return mock


def test_is_terminal_returns_true() -> None:
    t = Terminal("a")
    assert t.is_terminal() is True


def test_to_code_returns_value() -> None:
    t = Terminal("a")
    assert t.to_code() == "a"


@pytest.mark.parametrize(
    "terminal,expected",
    [
        (Terminal("a"), 'Terminal("a")'),
        (Terminal(0), 'Terminal("0")'),
    ],
)
def test_single_op_str_returns_expected(terminal: Terminal, expected: str) -> None:
    assert str(terminal) == expected
