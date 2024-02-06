from dataclasses import dataclass

from gsdl.model.dense_matrix import DenseMatrix


@dataclass
class Composition:
    A: DenseMatrix
    B: DenseMatrix

    def __post_init__(self):
        if not self.A.num_rows == self.B.num_rows:
            raise Exception(
                f"A rows ({self.A.num_rows}) does not match B rows ({self.B.num_rows})"
            )
