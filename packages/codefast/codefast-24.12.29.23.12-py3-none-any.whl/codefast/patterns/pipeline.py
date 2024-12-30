from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar('T')


class Pipeline(Generic[T], ABC):
    def __init__(self) -> None:
        self._previous = None

    @abstractmethod
    def process(self, data: Any) -> Any:
        pass

    def __or__(self, other: 'Pipeline') -> 'Pipeline':
        other._previous = self
        return other

    def execute(self, data: Any) -> Any:
        if self._previous:
            data = self._previous.execute(data)
        return self.process(data)


# Example implementations
class ExtractNumbers(Pipeline[str]):
    def process(self, data: str) -> list[int]:
        return [int(x) for x in data.split() if x.isdigit()]


class CalculateAverage(Pipeline[list]):
    def process(self, data: list[int]) -> float:
        return sum(data) / len(data)


class FormatResult(Pipeline[float]):
    def process(self, data: float) -> str:
        return f"Average is: {data:.2f}"


# Usage example
if __name__ == "__main__":
    # Create pipeline: extract numbers -> calculate average -> format result
    pipeline = ExtractNumbers() | CalculateAverage() | FormatResult()

    # Execute pipeline
    text = "The numbers are 10 20 30 40"
    result = pipeline.execute(text)
    print(result)  # Outputs: "Average is: 25.00"
