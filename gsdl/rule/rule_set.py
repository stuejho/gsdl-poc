import typing
from copy import deepcopy

from gsdl.operation import IOperation
from gsdl.parameter import IParam
from gsdl.rule import IRule
from gsdl.set_builder import SetBuilder


class RuleSet:
    def __init__(self, rules: list[IRule]):
        self.__rules = list(rules)

    def rules(self):
        return list(self.__rules)

    def get_first_matching_rule(self, operation: IOperation) -> IRule | None:
        result = None
        for rule in self.rules():
            if not isinstance(rule.get_lhs(), operation.__class__):
                continue

            rule_copy = self.__rule_with_operation_values(rule, operation)
            if self.__operation_matches_rule(operation, rule_copy):
                result = rule_copy
                break
        return result

    def get_matching_rules(self, operation: IOperation) -> list[IRule]:
        result = []
        for rule in self.rules():
            if not isinstance(rule.get_lhs(), operation.__class__):
                continue

            rule_copy = self.__rule_with_operation_values(rule, operation)
            if self.__operation_matches_rule(operation, rule_copy):
                rule_param_set = rule_copy.get_parameter_set()
                if rule_param_set:
                    values_set = rule_param_set.generate_set()
                    for value_set in values_set:
                        value_set_dict = SetBuilder.to_dict(value_set)
                        rule_copy_copy = deepcopy(rule_copy)
                        rule_copy_copy.set_param_values(value_set_dict)
                        result.append(rule_copy_copy)
                else:
                    result.append(rule_copy)
        return result

    def __rule_with_operation_values(self, rule: IRule, operation: IOperation) -> IRule:
        rule_copy = deepcopy(rule)

        rename_map = self.__get_rename_map(
            operation.get_params(), rule_copy.get_lhs().get_params()
        )
        renamed_param_values = self.__rename_param_values(
            operation.get_param_values(), rename_map
        )

        rule_copy.set_param_values(renamed_param_values)
        return rule_copy

    @staticmethod
    def __get_rename_map(
        from_params: list[IParam], to_params: list[IParam]
    ) -> dict[str, str]:
        rename_map = {}

        params_iter: typing.Iterator[tuple[IParam, IParam]] = zip(
            from_params, to_params
        )
        for from_param, to_param in params_iter:
            rename_map[from_param.get_name()] = to_param.get_name()
        return rename_map

    @staticmethod
    def __rename_param_values(param_values: dict[str, any], rename_map: dict[str, str]):
        renamed_values = {}
        for name, value in param_values.items():
            renamed_values[rename_map[name]] = value
        return renamed_values

    @staticmethod
    def __operation_matches_rule(operation: IOperation, rule: IRule) -> bool:
        return (type(operation) is type(rule.get_lhs())) and (
            (rule.get_condition() is None) or (rule.get_condition().evaluate())
        )
