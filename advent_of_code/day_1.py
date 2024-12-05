from pathlib import Path
from typing import Any
from advent_of_code import ASSETS_DIR
import numpy as np


def main():
    print(f"Running script {Path(__file__).name}...")

    # Task 1
    lh_col = get_sorted_col(0)
    assert lh_col.shape == (1000,), f"input file is 1000 lines long - got {lh_col.shape}"
    rh_col = get_sorted_col(1)
    abs_differences = [abs(a - b) for (a, b) in zip(lh_col, rh_col)]
    print(f"Total difference = {int(sum(abs_differences))}")

    # Task 2
    lh_unique_counts = np.unique_counts(lh_col)
    similarity_scores = [
        a * count_for(a, lh_unique_counts) * count_for(a, np.unique_counts(rh_col))
        for a in lh_unique_counts.values
    ]
    print(f"Similarity score = {int(sum(similarity_scores))}")


def count_for(val: int, unique_counts: Any) -> int:
    val_idx = np.where(unique_counts.values == val)[0]
    msg = f"input array must have unique values, {val_idx.shape=}"
    assert val_idx.size == 0 or val_idx.shape == (1,), msg
    return 0 if val_idx.size == 0 else int(unique_counts.counts[val_idx[0]])


def get_sorted_col(idx: int) -> np.ndarray[Any, np.dtype[np.float64]]:
    col = np.loadtxt(ASSETS_DIR / "day_1.txt", usecols=idx)
    col.sort()
    return col


if __name__ == "__main__":
    main()
