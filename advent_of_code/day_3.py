import logging
from pathlib import Path
import re
from advent_of_code import ASSETS_DIR
from advent_of_code.utils import solve, test_multiple, parse_args, configure_logging

TEST_SAMPLE_PART_1 = [
    "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))",
    "xmul(2,4)&mul[3,7]!^don't()?mul(8,5))",
]
EXPECTED_PART_1 = [161, 48]
TEST_SAMPLE_PART_2 = (
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
    48,
)


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    with open(ASSETS_DIR / "day_3.txt") as f:
        inputs = "".join(f.readlines())

    test_multiple(TEST_SAMPLE_PART_1, part_1_solver, "part 1", EXPECTED_PART_1)
    solve(inputs, part_1_solver, "part 1")
    test_multiple([TEST_SAMPLE_PART_2[0]], part_2_solver, "part 2", [TEST_SAMPLE_PART_2[1]])
    solve(inputs, part_2_solver, "part 2")


def part_1_solver(inputs: str) -> int:
    """Find all "mul(x,y) in a string and do the multiplication of x and y"""
    matches = re.findall(r"(?:mul\()(\d+)[,](\d+)[\)]", inputs)
    multiplications = [int(match[0]) * int(match[1]) for match in matches]
    return sum(multiplications)


def part_2_solver(inputs: str) -> int:
    first_section_match = re.match(r"(.*?)(?:don't\(\))", inputs, re.DOTALL)
    assert first_section_match, "Missing match for first section... is input correct?"
    first_section = first_section_match.group()
    remaining_sections = re.findall(r"(?:do\(\))(.*?)(?:don't\(\)|$)", inputs, re.DOTALL)
    string_to_search = "".join([first_section] + remaining_sections)
    return part_1_solver(string_to_search)


if __name__ == "__main__":
    main()
