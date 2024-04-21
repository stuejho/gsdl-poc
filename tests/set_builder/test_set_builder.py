from gsdl.generator import IntGenerator
from gsdl.parameter import IntParam
from gsdl.set_builder import SetBuilder


def test_constructor():
    x = IntParam("x")
    y = IntParam("y")
    m = IntParam("z").set_value(2)
    parameter_set = SetBuilder(
        (x, y),
        ((x, IntGenerator(0, m, 1)), (y, IntGenerator(0, m, 1))),
        (x + y == m),
    )
    assert parameter_set is not None


def test_generate_set():
    x = IntParam("x")
    y = IntParam("y")
    m = IntParam("z").set_value(5)
    parameter_set = SetBuilder(
        (x, y),
        ((x, IntGenerator(0, m, 1)), (y, IntGenerator(0, m, 1))),
        (x + y == m),
    )
    set_generator = parameter_set.generate_set()
    assert set_generator is not None

    result = list(set_generator)
    assert len(result) == 4

    assert result[0][0].get_name() == "x"
    assert result[0][0].get_value() == 1
    assert result[0][1].get_name() == "y"
    assert result[0][1].get_value() == 4

    assert result[1][0].get_name() == "x"
    assert result[1][0].get_value() == 2
    assert result[1][1].get_name() == "y"
    assert result[1][1].get_value() == 3

    assert result[2][0].get_name() == "x"
    assert result[2][0].get_value() == 3
    assert result[2][1].get_name() == "y"
    assert result[2][1].get_value() == 2

    assert result[3][0].get_name() == "x"
    assert result[3][0].get_value() == 4
    assert result[3][1].get_name() == "y"
    assert result[3][1].get_value() == 1
