from gsdl.operation import Repeat
from gsdl.parameter import IntParam


def test_constructor():
    r = Repeat(5)
    assert r is not None

    r_with_param = Repeat(IntParam("m"))
    assert r_with_param is not None
