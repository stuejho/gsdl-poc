from abc import ABC, abstractmethod


class IImplementation(ABC):
    @abstractmethod
    def to_code(self) -> str:
        raise NotImplementedError
