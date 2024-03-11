import itertools
from typing import Iterator

from gsdl.condition import ICondition
from gsdl.generator import IGenerator
from gsdl.parameter import IParam
from gsdl.set_builder import ISetBuilder


class SetBuilder(ISetBuilder):
    def __init__(
        self,
        parameters: tuple[IParam, ...],
        generator_tuples: tuple[[IParam, IGenerator], ...],
        predicate: ICondition,
    ):
        self.parameters = parameters
        self.generator_tuples = generator_tuples
        self.predicate = predicate

    def generate_set(self) -> Iterator[tuple[IParam, ...]]:
        parameterized_generators = [
            self._parameterize_generator(*g_tuple) for g_tuple in self.generator_tuples
        ]
        candidate_parameters: Iterator[tuple[IParam, ...]] = itertools.product(
            *parameterized_generators
        )

        predicate = self.predicate
        # TODO: This is messy, refactor it
        for cand_params in candidate_parameters:
            for pred_param in predicate.get_params():
                for cand_param in cand_params:
                    if pred_param.get_name() == cand_param.get_name():
                        pred_param.set_value(cand_param.get_value())
            if predicate.evaluate():
                yield cand_params

    @staticmethod
    def _parameterize_generator(
        param: IParam, generator: IGenerator
    ) -> Iterator[IParam]:
        return generator.generate(param)
