from abc import ABC, abstractmethod
from typing import Iterator

from gsdl.parameter import IParam


class IGenerator(ABC):
    @abstractmethod
    def generate(self, param: IParam) -> Iterator[IParam]:
        raise NotImplementedError