import pytest

from gsdl.operation import AbstractOperation, IOperation, Wrap
from gsdl.parameter import IParam, Param


class MockOperation(AbstractOperation):
    def __init__(
        self,
        params: list[IParam] = None,
        inputs: list[IOperation] = None,
        is_terminal: bool = False,
        is_base_case: bool = False,
    ):
        super().__init__(params, inputs, is_terminal, is_base_case)


def test_constructor_no_args_constructs_operation():
    mock_operation = MockOperation()
    assert mock_operation is not None


def test_add_combines_operations():
    a = MockOperation()
    b = MockOperation()
    c = MockOperation()

    res = a + b + c

    res_a = res
    res_b = res.get_next()
    res_c = res_b.get_next()

    assert res_a.get_next() is not None
    assert res_b.get_next() is not None
    assert res_c.get_next() is None

    assert res_a._prev_op is None
    assert res_b._prev_op is res_a
    assert res_c._prev_op is res_b


def test_get_next_no_join_returns_none():
    mock_operation = MockOperation()
    assert mock_operation.get_next() is None


@pytest.mark.parametrize("constructor_params", [([]), ([Param("x")])])
def test_get_params_returns_expected_copy(constructor_params: list[IParam]):
    mock_operation = MockOperation(params=constructor_params)
    operation_params = mock_operation.get_params()
    assert operation_params is not constructor_params
    assert len(operation_params) == len(constructor_params)


@pytest.mark.parametrize(
    "params,expected_values", [([], {}), ([Param("x")], {"x": None})]
)
def test_get_param_values_returns_expected_values(
    params: list[IParam], expected_values: dict
):
    mock_operation = MockOperation(params=params)
    param_values = mock_operation.get_param_values()

    assert param_values == expected_values


@pytest.mark.parametrize(
    "operation,expected",
    [
        (
            MockOperation() + MockOperation(),
            "MockOperation([], []) + MockOperation([], [])",
        )
    ],
)
def test_str_returns_expected_string(operation: AbstractOperation, expected: str):
    assert str(operation) == expected


@pytest.mark.parametrize(
    "operation,expected",
    [
        (
            MockOperation(),
            "MockOperation([], [])",
        ),
        (
            MockOperation(
                params=[Param("a").set_value("a"), Param("b").set_value("b")]
            ),
            "MockOperation([a, b], [])",
        ),
        (
            MockOperation(inputs=[MockOperation()]),
            "MockOperation([], [MockOperation([], [])])",
        ),
    ],
)
def test_single_op_str_returns_expected_string(
    operation: AbstractOperation, expected: str
):
    assert operation.single_op_str() == expected


@pytest.mark.parametrize(
    "operation,expected",
    [
        (MockOperation(is_terminal=False), False),
        (MockOperation(is_terminal=True), True),
        (MockOperation(is_base_case=False), False),
        (MockOperation(is_base_case=True), True),
        (MockOperation(is_terminal=False) + MockOperation(is_terminal=True), False),
        (MockOperation(is_terminal=True) + MockOperation(is_terminal=False), False),
        (MockOperation(is_terminal=True) + MockOperation(is_terminal=True), True),
        (MockOperation(is_base_case=False) + MockOperation(is_base_case=True), False),
        (MockOperation(is_base_case=True) + MockOperation(is_base_case=False), False),
        (MockOperation(is_base_case=True) + MockOperation(is_base_case=True), True),
        (
            MockOperation(is_terminal=True, inputs=[MockOperation(is_terminal=False)]),
            False,
        ),
        (
            MockOperation(is_terminal=False, inputs=[MockOperation(is_terminal=True)]),
            False,
        ),
        (
            MockOperation(is_terminal=True, inputs=[MockOperation(is_terminal=True)]),
            True,
        ),
        (
            MockOperation(
                is_base_case=True, inputs=[MockOperation(is_base_case=False)]
            ),
            False,
        ),
        (
            MockOperation(
                is_base_case=False, inputs=[MockOperation(is_base_case=True)]
            ),
            False,
        ),
        (
            MockOperation(is_base_case=True, inputs=[MockOperation(is_base_case=True)]),
            True,
        ),
    ],
)
def test_is_implementation(operation: AbstractOperation, expected: bool):
    assert operation.is_implementation() == expected


@pytest.mark.parametrize(
    "operation,expected",
    [
        (MockOperation(is_terminal=False), False),
        (MockOperation(is_terminal=True), True),
    ],
)
def test_is_terminal(operation: AbstractOperation, expected: bool):
    assert operation.is_implementation() == expected


@pytest.mark.parametrize(
    "operation,expected",
    [
        (MockOperation(is_base_case=False), False),
        (MockOperation(is_base_case=True), True),
    ],
)
def test_is_base_case(operation: AbstractOperation, expected: bool):
    assert operation.is_implementation() == expected


def test_get_first_non_terminal_with_terminal_returns_none():
    mock_operation = MockOperation(is_terminal=True)
    assert mock_operation.get_first_non_terminal() is None


def test_get_first_non_terminal_with_non_terminal_returns_itself():
    mock_operation = MockOperation(is_terminal=False)
    assert mock_operation.get_first_non_terminal() is mock_operation


@pytest.mark.parametrize(
    "a,b,c,expected_index",
    [
        (
            MockOperation(is_terminal=False),
            MockOperation(is_terminal=False),
            MockOperation(is_terminal=False),
            0,
        ),
        (
            MockOperation(is_terminal=True),
            MockOperation(is_terminal=False),
            MockOperation(is_terminal=False),
            1,
        ),
        (
            MockOperation(is_terminal=True),
            MockOperation(is_terminal=True),
            MockOperation(is_terminal=False),
            2,
        ),
    ],
)
def test_get_first_non_terminal_in_next(
    a: AbstractOperation,
    b: AbstractOperation,
    c: AbstractOperation,
    expected_index: int,
):
    res = a + b + c
    expected = res
    while expected_index > 0:
        expected = expected.get_next()
        expected_index -= 1
    assert res.get_first_non_terminal() is expected


@pytest.mark.parametrize(
    "x,y,z,expected_index",
    [
        (
            MockOperation(is_terminal=False),
            MockOperation(is_terminal=False),
            MockOperation(is_terminal=False),
            0,
        ),
        (
            MockOperation(is_terminal=True),
            MockOperation(is_terminal=False),
            MockOperation(is_terminal=False),
            1,
        ),
        (
            MockOperation(is_terminal=True),
            MockOperation(is_terminal=True),
            MockOperation(is_terminal=False),
            2,
        ),
    ],
)
def test_get_first_non_terminal_in_inputs(
    x: AbstractOperation,
    y: AbstractOperation,
    z: AbstractOperation,
    expected_index: int,
):
    mock_operation = MockOperation(inputs=[x, y, z])
    assert (
        mock_operation.get_first_non_terminal()
        is mock_operation._inputs[expected_index]
    )


def test_expand_operation_non_nested_lhs():
    a = MockOperation()
    b = MockOperation()
    c = MockOperation()

    res = a + b + c
    res_expected_next_op = res.get_next()
    res_expected_next_join_op = res._next_join_op
    res.expand_operation(MockOperation())

    assert res._parent_op is None
    assert res._parent_op_idx is None
    assert res._prev_op is None
    assert res._next_op is res_expected_next_op
    assert res._next_join_op is res_expected_next_join_op


def test_expand_operation_nested_input_lhs():
    x = MockOperation()
    y = MockOperation()
    z = MockOperation()

    res = MockOperation(inputs=[x + y + z])
    target = res._inputs[0]
    target_expected_next_op = target._next_op
    target_expected_next_join_op = target._next_join_op
    target.expand_operation(MockOperation())

    assert target._parent_op is res
    assert target._parent_op_idx is 0
    assert target._prev_op is None
    assert target._next_op is target_expected_next_op
    assert target._next_join_op is target_expected_next_join_op

    assert isinstance(res._inputs[0], Wrap)


def test_expand_operation_nested_input_non_lhs():
    x = MockOperation()
    y = MockOperation()
    z = MockOperation()

    res = MockOperation(inputs=[x + y + z])
    target = res._inputs[0]._next_op
    target_expected_prev_op = target._prev_op
    target_expected_next_op = target._next_op
    target_expected_next_join_op = target._next_join_op
    target.expand_operation(MockOperation())

    assert target._parent_op is None
    assert target._parent_op_idx is None
    assert target._prev_op is target_expected_prev_op
    assert target._next_op is target_expected_next_op
    assert target._next_join_op is target_expected_next_join_op

    assert isinstance(res._inputs[0]._next_op, Wrap)
