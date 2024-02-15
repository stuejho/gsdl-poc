from abc import ABC, abstractmethod


class IJoin(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError
