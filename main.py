from gsdl.algorithm import Algorithm
from gsdl.condition import GreaterThan
from gsdl.operation import Repeat, Terminal
from gsdl.parameter import IntParam, Param
from gsdl.rule import Rule, RuleSet


def main():
    m = IntParam("m")

    rules = [
        Rule(Repeat(m), Repeat(m - 1) + Repeat(1), condition=GreaterThan(m, 1)),
        Rule(Repeat(1, is_base_case=True), Terminal("a")),
    ]
    rule_set = RuleSet(rules)

    z = IntParam("m")
    z.set_value(5)
    r = Repeat(z)
    a = Algorithm(r, rule_set)
    print(a.to_algorithm())


if __name__ == "__main__":
    main()
