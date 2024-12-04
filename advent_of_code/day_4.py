from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from advent_of_code import ASSETS_DIR
from advent_of_code.utils import solve, test

TEST_SAMPLE_BOTH_PARTS = [
    [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX",
    ]
]
EXPECTED_PART_1 = [18]
EXPECTED_PART_2 = [9]


@dataclass
class Index:
    row: int
    col: int


def main():
    print(f"Running script {Path(__file__).name}...")
    with open(ASSETS_DIR / "day_4.txt") as f:
        input = list(f.readlines())

    test(TEST_SAMPLE_BOTH_PARTS, part_1, "Test part 1", EXPECTED_PART_1)
    solve(input, part_1, "Part 1", expected=2571)
    test(TEST_SAMPLE_BOTH_PARTS, part_2, "Test part 2", EXPECTED_PART_2)
    solve(input, part_2, "Part 2", expected=1992)


def part_1(input: list[str]) -> int:
    total = 0
    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if char == "X":
                words_possible = [
                    word_from_grid(input, Index(row, col), dir, length=4) for dir in Direction
                ]
                total += len([w for w in words_possible if w == "XMAS"])
    return total


def part_2(input: list[str]) -> int:
    total = 0
    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if char == "A" and cross_mas_found(input, Index(row, col)):
                total += 1
    return total


def cross_mas_found(input: list[str], idx: Index) -> bool:
    accepgrid_words = ["MAS", "SAM"]
    se_word = word_from_grid(input, increment_idx(idx, Direction.NW), Direction.SE, length=3)
    nw_word = word_from_grid(input, increment_idx(idx, Direction.NE), Direction.SW, length=3)
    return se_word in accepgrid_words and nw_word in accepgrid_words


class Direction(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7


ALL_DIRECTIONS = [e for e in Direction]

INCREMENET_FUNC = {
    Direction.N: lambda idx: Index(idx.row - 1, idx.col),
    Direction.NE: lambda idx: Index(idx.row - 1, idx.col + 1),
    Direction.E: lambda idx: Index(idx.row, idx.col + 1),
    Direction.SE: lambda idx: Index(idx.row + 1, idx.col + 1),
    Direction.S: lambda idx: Index(idx.row + 1, idx.col),
    Direction.SW: lambda idx: Index(idx.row + 1, idx.col - 1),
    Direction.W: lambda idx: Index(idx.row, idx.col - 1),
    Direction.NW: lambda idx: Index(idx.row - 1, idx.col - 1),
}


def increment_idx(idx: Index, direction: Direction) -> Index:
    incrementer = INCREMENET_FUNC[direction]
    return incrementer(idx)


def word_from_grid(grid: list[str], start: Index, direction: Direction, length: int) -> str:
    if out_of_range(grid, start):
        return ""
    idx = start
    word = ""
    for _ in range(length):
        word += get_char(grid, idx)
        idx = increment_idx(idx, direction)
        if out_of_range(grid, idx):
            break
    return word


def get_char(grid: list[str], idx: Index) -> str:
    try:
        return grid[idx.row][idx.col]
    except IndexError:
        raise IndexError(f"Could access {idx = }")


def out_of_range(grid: list[str], idx: Index) -> bool:
    if idx.row >= len(grid) or idx.col >= len(grid[0]) or min(idx.col, idx.row) < 0:
        return True
    return False


if __name__ == "__main__":
    main()