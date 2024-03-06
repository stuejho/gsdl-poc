from __future__ import annotations

from abc import ABC, abstractmethod

from gsdl.condition import ICondition
from gsdl.operation import IOperation


class IRule(ABC):
    @abstractmethod
    def get_lhs(self) -> IOperation:
        raise NotImplementedError

    @abstractmethod
    def get_rhs(self) -> IOperation:
        raise NotImplementedError

    @abstractmethod
    def get_condition(self) -> ICondition:
        raise NotImplementedError

    @abstractmethod
    def set_param_values(self, param_values: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def can_evaluate(self, param_values: dict) -> bool:
        raise NotImplementedError
