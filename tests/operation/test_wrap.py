from unittest.mock import patch, Mock

import pytest

from gsdl.operation import Wrap, IOperation


@pytest.fixture
@patch.multiple(IOperation, __abstractmethods__=set())
def operation() -> IOperation:
    mock = Mock(spec=IOperation)
    mock.__str__ = Mock(return_value="operation")
    return mock


def test_single_op_str_returns_parenthesized_operation_str(
    operation: IOperation,
) -> None:
    wrap = Wrap(operation)

    assert str(wrap) == "(operation)"
