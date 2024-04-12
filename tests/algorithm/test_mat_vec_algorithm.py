import pytest

from gsdl.algorithm import Algorithm
from gsdl.operation import MatVec, MatVecUnblockedRow, MatVecUnblockedCol
from gsdl.parameter import IntParam
from gsdl.rule import Rule, RuleSet

@pytest.mark.parametrize(
    "num_rows,num_cols,expected_num_expansions",
    [
        (4, 4, 2)
    ]
)
def test_mat_vec_unblocked_rules(num_rows, num_cols, expected_num_expansions):
    m = IntParam("m")
    n = IntParam("n")

    rules = [
        Rule(MatVec(m, n), MatVecUnblockedRow(0, m, 0, n)),
        Rule(MatVec(m, n), MatVecUnblockedCol(0, m, 0, n)),
    ]
    rule_set = RuleSet(rules)

    repeat = MatVec(num_rows, num_cols)
    a = Algorithm(repeat, rule_set)

    expansions = a.all_expansions()
    for e in expansions:
        print(e)
        print(e.to_code())

    assert len(expansions) == expected_num_expansions
