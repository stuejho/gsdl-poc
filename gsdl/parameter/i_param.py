from abc import abstractmethod
from typing import Self


class IParam:
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_value(self) -> any:
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value: any) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError
