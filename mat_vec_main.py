import subprocess
from typing import TextIO

from gsdl.algorithm import Algorithm
from gsdl.generator import IntGenerator
from gsdl.operation import (
    MatVecUnblockedRow,
    MatVecUnblockedCol,
    MatVec,
    MatVecBlockedRow,
    MatVecBlockedCol,
)
from gsdl.parameter import IntParam
from gsdl.rule import Rule, RuleSet
from gsdl.set_builder import SetBuilder


def main():
    num_rows = 4
    num_cols = 4

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

    with open("result.csv", "w") as result_file:
        result_file.write("Code,Total (ns),Average (ns)\n")
        for e in expansions:
            code = e.to_code()
            run_code(str(e), code, num_rows, num_cols, result_file)
    print(len(expansions))


def run_code(id: str, code: str, num_rows: int, num_cols: int, result_file: TextIO):
    with open("benchmark/matvec/benchmark.ctmpl", "r") as template_file:
        template_code = template_file.read()

    impl_code = template_code.replace("{{ benchmark_code }}", code)

    with open("benchmark/matvec/benchmark.c", "w") as benchmark_file:
        benchmark_file.write(impl_code)

    subprocess.run(
        ["make", f"M={num_rows}", f"N={num_cols}", f"num_rows={num_rows}", f"num_cols={num_cols}"],
        cwd="./benchmark/matvec",
        stdout=subprocess.DEVNULL,
        stderr=None,
    )

    print(id)
    print(code)
    result = subprocess.run(
        "./main.x",
        cwd="./benchmark/matvec",
        stdout=None,
        stderr=None,
        capture_output=True,
    )
    result_file.write(f'"{code}",')
    result_file.write(result.stdout.decode("utf-8"))


if __name__ == "__main__":
    main()
