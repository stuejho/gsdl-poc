from gsdl.algorithm import Algorithm
from gsdl.condition import GreaterThan, EqualTo
from gsdl.generator import IntGenerator
from gsdl.operation import Repeat, Terminal, MatVec, MatVecUnblockedRow, MatVecUnblockedCol
from gsdl.parameter import IntParam
from gsdl.rule import Rule, RuleSet
from gsdl.set_builder import SetBuilder


def main():
    m = IntParam("m")
    n = IntParam("n")

    rules = [
        Rule(MatVec(m, n), MatVecUnblockedRow(0, m, 0, n)),
        Rule(MatVec(m, n), MatVecUnblockedCol(0, m, 0, n)),
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
