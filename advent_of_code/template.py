import logging
from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test, parse_args, configure_logging


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day__sample.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=0)
    solve(inputs, part_1, "Part 1")


def parse_inputs(inputs: list[str]) -> list[str]:
    return []


def part_1(inputs: list[str]) -> int:
    return 0


if __name__ == "__main__":
    main()
