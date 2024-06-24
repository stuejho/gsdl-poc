from abc import ABC, abstractmethod

from gsdl.executor import ExecutionResult


class IExecutor(ABC):
    @abstractmethod
    def execute(self, run_id: str, code: str) -> ExecutionResult:
        raise NotImplementedError
