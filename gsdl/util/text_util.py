import textwrap


class TextUtil:
    SPACES_PER_INDENT = 4

    @staticmethod
    def dedent(text: str) -> str:
        return textwrap.dedent(text)

    @staticmethod
    def indent(text: str, prefix: str, predicate=None) -> str:
        return textwrap.indent(text, prefix, predicate)

    @classmethod
    def indent_by_level(cls, text: str, indent_level: int) -> str:
        return cls.indent(text, " " * cls.SPACES_PER_INDENT * indent_level)
