from __future__ import annotations

from abc import abstractmethod


class IParam:
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_value(self) -> any:
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value: any) -> IParam:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError
