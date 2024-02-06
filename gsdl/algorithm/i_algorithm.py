from abc import ABC, abstractmethod


class IAlgorithm(ABC):
    @staticmethod
    @abstractmethod
    def header(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def code(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def call(*args, **kwargs):
        raise NotImplementedError
