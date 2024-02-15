from gsdl.rule import IRule


class RuleSet:
    def __init__(self, rules: list[IRule]):
        self.__rules = list(rules)

    def rules(self):
        return list(self.__rules)
