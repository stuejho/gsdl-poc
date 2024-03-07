from abc import ABC, abstractmethod

from gsdl.parameter import IParam


class ICondition(ABC):
    @abstractmethod
    def get_params(self) -> list[IParam]:
        raise NotImplementedError

    @abstractmethod
    def is_match(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError
