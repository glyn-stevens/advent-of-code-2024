from pathlib import Path
from advent_of_code.utils import read_input, solve


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = read_input("day_5.txt")
    solve(inputs, part_1, "Part 1")


def part_1(inputs: list[str]) -> int:
    return 0


if __name__ == "__main__":
    main()
