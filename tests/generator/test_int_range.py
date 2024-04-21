import pytest

from gsdl.generator import IntGenerator
from gsdl.parameter import IntParam


@pytest.mark.parametrize(
    "int_range,expected_values",
    [
        (IntGenerator(0, 10, 1), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (
            IntGenerator(IntParam("x").set_value(0), 10, 1),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        (
            IntGenerator(0, IntParam("x").set_value(10), 1),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        (
            IntGenerator(0, 10, IntParam("x").set_value(1)),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
    ],
)
def test_generate(int_range: IntGenerator, expected_values: list[int]):
    m = IntParam("m")
    generator = int_range.generate(m)
    for idx, generated_param in enumerate(generator):
        assert generated_param.get_value() == expected_values[idx]
