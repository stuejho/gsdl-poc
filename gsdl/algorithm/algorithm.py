from dataclasses import dataclass

from gsdl.operation import IOperation, Wrap
from gsdl.rule.rule_set import RuleSet


@dataclass
class Algorithm:
    operation: IOperation
    rule_set: RuleSet

    def to_algorithm(self) -> IOperation:
        curr_expansion = Wrap(self.operation)

        while not curr_expansion.is_implementation():
            print("Current expansion:\t", curr_expansion)

            curr_op = curr_expansion.get_first_non_terminal()
            print("Current operation:\t", curr_op.single_op_str())

            rule = self.rule_set.get_first_matching_rule(curr_op)
            print("Apply rule:\t\t\t", rule)

            curr_op.expand_operation(rule.get_rhs())

            print()
        return curr_expansion

    def all_expansions(self) -> list[IOperation]:
        init_expansion = Wrap(self.operation)

        frontier = [init_expansion]
        result = []

        while frontier:
            curr_expansion = frontier.pop()
            print("Current expansion:\t", curr_expansion)

            curr_op = curr_expansion.get_first_non_terminal()
            print("Current operation:\t", curr_op.single_op_str())

            rules = self.rule_set.get_matching_rules(curr_op)
            for rule in rules:
                expansion_copy = curr_expansion.copy()
                curr_op_copy = expansion_copy.get_first_non_terminal()
                print("Apply rule:\t\t\t", rule)

                curr_op_copy.expand_operation(rule.get_rhs())
                if expansion_copy.is_implementation():
                    result.append(expansion_copy)
                else:
                    frontier.append(expansion_copy)
        return result

    def to_code(self) -> str:
        algo = self.to_algorithm()

        return algo.to_code()
