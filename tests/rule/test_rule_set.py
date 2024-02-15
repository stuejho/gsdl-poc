from gsdl.rule import RuleSet


def test_constructor() -> None:
    rule_set = RuleSet([])
    assert rule_set is not None


def test_rules_returns_copy() -> None:
    input_rules = []
    rule_set = RuleSet(input_rules)

    result_rules = rule_set.rules()

    assert input_rules is not result_rules
