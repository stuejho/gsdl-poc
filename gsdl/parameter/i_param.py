from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Self

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gsdl.condition import ICondition


class IParam(ABC):
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_value(self) -> any:
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value: any) -> Self:
        raise NotImplementedError

    def get_params(self) -> list[Self]:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other: any) -> IParam:
        raise NotImplementedError

    @abstractmethod
    def __sub__(self, other: any) -> IParam:
        raise NotImplementedError

    @abstractmethod
    def __mul__(self, other: any) -> IParam:
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other: any) -> ICondition:
        raise NotImplementedError

    @abstractmethod
    def __gt__(self, other: any) -> ICondition:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: any) -> ICondition:
        raise NotImplementedError
