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

    def to_code(self) -> str:
        algo = self.to_algorithm()

        return algo.to_code()
