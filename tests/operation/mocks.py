from gsdl.operation import AbstractOperation
from gsdl.parameter import IntParam


class MockNonTerminalA(AbstractOperation):
    pass


class MockNonTerminalB(AbstractOperation):
    pass


class MockNonTerminalC(AbstractOperation):
    pass


class MockRepeat(AbstractOperation):
    def __init__(self, times: IntParam | int, is_base_case: bool = False):
        if isinstance(times, int):
            t = IntParam("const").set_value(times)
        else:
            t = times
        super().__init__([t], is_base_case=is_base_case)


class MockTerminal(AbstractOperation):
    def __init__(self):
        super().__init__(is_terminal=True)

    def to_code(self) -> str:
        return "a"
