from dataclasses import dataclass


@dataclass
class ExecutionResult:
    """Record storing execution result."""

    """Result id."""
    id: str

    """Executed code."""
    code: str

    """Command line output."""
    result: str
