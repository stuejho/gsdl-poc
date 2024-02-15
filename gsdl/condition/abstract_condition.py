from abc import ABC
from typing import Callable

from gsdl.condition import ICondition
from gsdl.parameter import IParam


class AbstractCondition(ICondition, ABC):
    def __init__(self, params: list[IParam], condition: Callable[..., bool]):
        self.params = list(params)
        self.condition = condition

    def get_params(self) -> list[IParam]:
        return list(self.params)

    def is_match(self):
        return self.condition(*self.params)
