from copy import deepcopy
from dataclasses import dataclass

from gsdl.operation import IOperation, Wrap
from gsdl.rule import IRule
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

            param_values = curr_op.get_param_values()
            rule = self.__get_matching_rule(curr_op, param_values)
            print("Apply rule:\t\t\t", rule)

            curr_op.expand_operation(rule.get_rhs())

            print()
        return curr_expansion

    def to_code(self):
        return "TODO"

    def __get_matching_rule(
        self, operation: IOperation, param_values: dict
    ) -> IRule | None:
        for rule in self.rule_set.rules():
            rule_copy = deepcopy(rule)
            if not rule_copy.can_evaluate(param_values):
                continue
            rule_copy.set_param_values(param_values)
            if self.__operation_matches_rule(operation, rule_copy):
                return rule_copy
        return None

    @staticmethod
    def __operation_matches_rule(operation: IOperation, rule: IRule) -> bool:
        return (type(operation) is type(rule.get_lhs())) and (
            (rule.get_condition() is None) or (rule.get_condition().is_match())
        )
