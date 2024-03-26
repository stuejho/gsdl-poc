from typing import Iterator

from gsdl.generator import IGenerator
from gsdl.parameter import IntParam, IParam


class IntGenerator(IGenerator):
    def __init__(
        self, start: IntParam | int, stop: IntParam | int, step: IntParam | int
    ):
        self.start = start
        self.stop = stop
        self.step = step

    def generate(self, param: IParam) -> Iterator[IParam]:
        start = self._evaluate_start()
        stop = self._evaluate_stop()
        step = self._evaluate_step()
        for i in range(start, stop, step):
            yield IntParam(param.get_name()).set_value(i)

    def _evaluate_start(self):
        if isinstance(self.start, IntParam):
            return self.start.get_value()
        return self.start

    def _evaluate_stop(self):
        if isinstance(self.stop, IntParam):
            return self.stop.get_value()
        return self.stop

    def _evaluate_step(self):
        if isinstance(self.step, IntParam):
            return self.step.get_value()
        return self.step

    def get_params(self) -> list[IParam]:
        result = []

        if isinstance(self.start, IParam):
            result.append(self.start)
        if isinstance(self.stop, IParam):
            result.append(self.stop)
        if isinstance(self.step, IParam):
            result.append(self.step)

        return result
