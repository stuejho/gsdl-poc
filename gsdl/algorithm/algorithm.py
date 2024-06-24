from dataclasses import dataclass
from typing import Iterator

from gsdl.operation import IOperation, Wrap
from gsdl.rule.rule_set import RuleSet


@dataclass
class Algorithm:
    operation: IOperation
    rule_set: RuleSet

    def to_algorithm(self) -> IOperation:
        curr_expansion = Wrap(self.operation)

        while not curr_expansion.is_implementation():
            curr_op = curr_expansion.get_first_non_terminal()

            rule = self.rule_set.get_first_matching_rule(curr_op)

            curr_op.expand_operation(rule.get_rhs())
        return curr_expansion

    def all_expansions(self) -> list[IOperation]:
        init_expansion = Wrap(self.operation)

        frontier = [init_expansion]
        result = []

        while frontier:
            curr_expansion = frontier.pop()

            curr_op = curr_expansion.get_first_non_terminal()

            rules = self.rule_set.get_matching_rules(curr_op)
            for rule in rules:
                expansion_copy = curr_expansion.copy()
                curr_op_copy = expansion_copy.get_first_non_terminal()

                curr_op_copy.expand_operation(rule.get_rhs())
                expansion_copy.set_parent_expansion(curr_expansion)
                if expansion_copy.is_implementation():
                    # print("Final expansion:\t", expansion_copy)
                    result.append(expansion_copy)
                else:
                    frontier.append(expansion_copy)
        return result

    def all_expansions_generator(self) -> Iterator[IOperation]:
        init_expansion = Wrap(self.operation)

        frontier = [init_expansion]

        while frontier:
            curr_expansion = frontier.pop()

            curr_op = curr_expansion.get_first_non_terminal()

            rules = self.rule_set.get_matching_rules(curr_op)
            for rule in rules:
                expansion_copy = curr_expansion.copy()
                curr_op_copy = expansion_copy.get_first_non_terminal()

                curr_op_copy.expand_operation(rule.get_rhs())
                expansion_copy.set_parent_expansion(curr_expansion)
                if expansion_copy.is_implementation():
                    yield expansion_copy
                else:
                    frontier.append(expansion_copy)

    def to_code(self) -> str:
        algo = self.to_algorithm()

        return algo.to_code()
