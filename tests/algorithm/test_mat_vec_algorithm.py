import pytest

from gsdl.algorithm import Algorithm
from gsdl.condition import GreaterThan
from gsdl.generator import IntGenerator
from gsdl.operation import (
    MatVec,
    MatVecUnblockedRow,
    MatVecUnblockedCol,
    MatVecBlockedRow,
    MatVecBlockedCol,
)
from gsdl.parameter import IntParam
from gsdl.rule import Rule, RuleSet
from gsdl.set_builder import SetBuilder


@pytest.mark.parametrize("num_rows,num_cols,expected_num_expansions", [(4, 4, 2)])
def test_mat_vec_unblocked_rules(num_rows, num_cols, expected_num_expansions):
    m = IntParam("m")
    n = IntParam("n")

    rules = [
        Rule(MatVec(m, n), MatVecUnblockedRow(m, n)),
        Rule(MatVec(m, n), MatVecUnblockedCol(m, n)),
    ]
    rule_set = RuleSet(rules)

    repeat = MatVec(num_rows, num_cols)
    a = Algorithm(repeat, rule_set)

    expansions = a.all_expansions()
    for e in expansions:
        print(e)
        print(e.to_code())

    assert len(expansions) == expected_num_expansions


@pytest.mark.parametrize("num_rows,num_cols,expected_num_expansions", [(4, 4, 2)])
def test_mat_vec_blocked_rules(num_rows, num_cols, expected_num_expansions):
    m = IntParam("m")
    n = IntParam("n")
    mb = IntParam("mb")
    nb = IntParam("nb")

    rules = [
        Rule(MatVec(m, n), MatVecUnblockedRow(m, n)),
        Rule(MatVec(m, n), MatVecUnblockedCol(m, n)),
        Rule(
            MatVec(m, n),
            MatVecBlockedRow(m, n, mb, MatVec(mb, n)),
            condition=(m > 1),
            parameter_set=SetBuilder(
                (mb,),
                (
                    (
                        mb,
                        IntGenerator(1, m, 1),
                    ),
                    (
                        nb,
                        IntGenerator(1, n, 1),
                    ),
                ),
                (m % mb == 0),
            ),
        ),
        Rule(
            MatVec(m, n),
            MatVecBlockedCol(m, n, nb, MatVec(m, nb)),
            condition=((n > 1)),
            parameter_set=SetBuilder(
                (nb,),
                (
                    (
                        nb,
                        IntGenerator(1, n, 1),
                    ),
                ),
                (n % nb == 0),
            ),
        ),
    ]
    rule_set = RuleSet(rules)

    repeat = MatVec(num_rows, num_cols)
    a = Algorithm(repeat, rule_set)

    expansions = a.all_expansions()
    for e in expansions:
        print(e)
        print(e.to_code())

    assert len(expansions) == expected_num_expansions
