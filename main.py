from gsdl.algorithm import Algorithm
from gsdl.condition import GreaterThan, EqualTo
from gsdl.generator import IntGenerator
from gsdl.operation import Repeat, Terminal
from gsdl.parameter import IntParam
from gsdl.rule import Rule, RuleSet
from gsdl.set_builder import SetBuilder


def main():
    m = IntParam("m")
    l = IntParam("l")
    k = IntParam("k")

    rules = [
        Rule(Repeat(m), Repeat(m - 1) + Repeat(1), condition=GreaterThan(m, 1)),
        Rule(
            Repeat(m),
            Repeat(l) + Repeat(k),
            condition=GreaterThan(m, 1),
            parameter_set=SetBuilder(
                (l, k),
                (
                    (
                        l,
                        IntGenerator(0, m, 1),
                    ),
                    (
                        k,
                        IntGenerator(0, m, 1),
                    ),
                ),
                l + k == m,
            ),
        ),
        Rule(Repeat(m), Terminal("a"), condition=EqualTo(m, 1)),
    ]
    rule_set = RuleSet(rules)

    repeat = Repeat(5)
    a = Algorithm(repeat, rule_set)

    expansions = a.all_expansions()

    for ex in expansions:
        print("Expansion:", ex)
        ex.print_cool_stuff()
        print(ex.to_code())
        print()


if __name__ == "__main__":
    main()
