from abc import ABC, abstractmethod


class IImplementation(ABC):
    @abstractmethod
    def to_code(self, *args, **kwargs) -> str:
        raise NotImplementedError
