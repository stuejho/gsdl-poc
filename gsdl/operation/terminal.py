from dataclasses import dataclass

from gsdl.operation import AbstractOperation


@dataclass
class Terminal(AbstractOperation):
    def __init__(self, value):
        super().__init__(is_terminal=True)
        self.value = value

    def to_code(self) -> str:
        return self.value

    def single_op_str(self):
        return f'Terminal("{self.value}")'
