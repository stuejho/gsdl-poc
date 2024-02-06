from dataclasses import dataclass


@dataclass
class DenseMatrix:
    """Dense matrix representation."""

    num_rows: int
    num_cols: int
    row_stride: int
    col_stride: int
    ptr_name: str
