from __future__ import annotations

from abc import ABC, abstractmethod

from gsdl.operation import IImplementation
from gsdl.parameter import IParam


class IOperation(IImplementation, ABC):

    @abstractmethod
    def get_params(self) -> list[IParam]:
        raise NotImplementedError

    @abstractmethod
    def get_inputs(self) -> list[IOperation]:
        raise NotImplementedError

    @abstractmethod
    def get_param_values(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def is_implementation(self) -> bool:
        """
        Returns whether an operation has been expanded to
        only include terminal/base cases.
        """
        raise NotImplementedError

    @abstractmethod
    def is_terminal(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_base_case(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_first_non_terminal(self) -> IOperation | None:
        raise NotImplementedError

    @abstractmethod
    def expand_operation(self, operation: IOperation) -> None:
        raise NotImplementedError

    @abstractmethod
    def single_op_str(self) -> str:
        raise NotImplementedError
