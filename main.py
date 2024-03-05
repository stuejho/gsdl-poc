from gsdl.algorithm import Algorithm
from gsdl.condition import GreaterThan
from gsdl.operation import Repeat, Terminal
from gsdl.parameter import IntParam
from gsdl.rule import Rule, RuleSet


def main():
    m = IntParam("m")

    rules = [
        Rule(Repeat(m), Repeat(m - 1) + Repeat(1), condition=GreaterThan(m, 1)),
        Rule(Repeat(1, is_base_case=True), Terminal("a")),
    ]
    rule_set = RuleSet(rules)

    repeat = Repeat(IntParam("m").set_value(5))
    a = Algorithm(repeat, rule_set)
    print(a.to_algorithm())
    print(a.to_code())


if __name__ == "__main__":
    main()
