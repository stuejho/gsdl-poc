import pytest

from gsdl.util import TextUtil


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", ""),
        ("abc", "abc"),
        (
            """
        abc
            def
        123
        """,
            """
abc
    def
123
""",
        ),
    ],
)
def test_dedent(text: str, expected: str) -> None:
    assert TextUtil.dedent(text) == expected


@pytest.mark.parametrize(
    "text,prefix,predicate,expected",
    [
        ("hello", "", None, "hello"),
        ("hello", "say ", None, "say hello"),
        ("hello", "say ", lambda x: True, "say hello"),
        ("", "empty", lambda x: False, ""),
    ],
)
def test_indent(text: str, prefix: str, predicate, expected: str) -> None:
    assert TextUtil.indent(text, prefix, predicate) == expected
