from pathlib import Path
from advent_of_code.utils import read_input, solve, test


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = read_input("day_.txt")
    sample_inputs = read_input("day__sample.txt")
    test(sample_inputs, part_1, "Part 1 test", expected=0)
    solve(inputs, part_1, "Part 1")


def part_1(inputs: list[str]) -> int:
    return 0


if __name__ == "__main__":
    main()
