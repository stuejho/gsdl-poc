from gsdl.join import Concat


def test_str() -> None:
    concat = Concat()

    assert str(concat) == "+"
