from abc import ABC, abstractmethod
from typing import Iterator

from gsdl.parameter import IParam


class ISetBuilder(ABC):
    @abstractmethod
    def generate_set(self) -> Iterator[tuple[IParam, ...]]:
        raise NotImplementedError

    @abstractmethod
    def get_params(self) -> list[IParam]:
        raise NotImplementedError
