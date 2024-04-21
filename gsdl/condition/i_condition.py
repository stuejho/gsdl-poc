from __future__ import annotations

from abc import ABC, abstractmethod

from gsdl.parameter import IParam


class ICondition(ABC):
    @abstractmethod
    def get_params(self) -> list[IParam]:
        raise NotImplementedError

    @abstractmethod
    def evaluate(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    def __and__(self, other: any) -> ICondition:
        raise NotImplementedError

    def __or__(self, other: any) -> ICondition:
        raise NotImplementedError
