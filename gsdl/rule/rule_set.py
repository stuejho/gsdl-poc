import typing
from copy import deepcopy

from gsdl.operation import IOperation
from gsdl.parameter import IParam
from gsdl.rule import IRule


class RuleSet:
    def __init__(self, rules: list[IRule]):
        self.__rules = list(rules)

    def rules(self):
        return list(self.__rules)

    def get_matching_rule(self, operation: IOperation) -> IRule | None:
        result = None
        param_values = operation.get_param_values()
        for rule in self.rules():
            if not isinstance(rule.get_lhs(), operation.__class__):
                continue

            rule_copy = deepcopy(rule)

            rename_map = self.__get_rename_map(
                operation.get_params(), rule_copy.get_lhs().get_params()
            )
            renamed_param_values = self.__rename_param_values(param_values, rename_map)

            rule_copy.set_param_values(renamed_param_values)
            if self.__operation_matches_rule(operation, rule_copy):
                result = rule_copy
                break
        return result

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
            (rule.get_condition() is None) or (rule.get_condition().is_match())
        )
