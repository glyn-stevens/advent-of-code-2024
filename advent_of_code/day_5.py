from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

from advent_of_code.utils import read_input, solve, test

EXPECT_PART_1 = [143]


@dataclass
class Rule:
    lower: int
    upper: int


Sample = list[int]


@dataclass
class ParsedInput:
    rules: list[Rule]
    samples: list[Sample]


def main():
    print(f"Running script {Path(__file__).name}...")
    sample_inputs = [read_input("day_5_sample.txt")]
    inputs = read_input("day_5.txt")
    test(sample_inputs, part_1, "PART 1 test", expected=EXPECT_PART_1)
    solve(inputs, part_1, "Part 1")
    # solve(inputs, part_2, "Part 2")


def part_1(inputs: list[str]) -> int:
    parsed_inputs = parse(inputs)
    passing_samples = [
        s for s in parsed_inputs.samples if sample_passes_rules(s, parsed_inputs.rules)
    ]
    middle_values = [s[int(len(s) / 2)] for s in passing_samples]
    return sum(middle_values)


def sample_passes_rules(sample: Sample, rules: list[Rule]) -> bool:
    return all(sample_passes_rule(sample, r) for r in rules)


def sample_passes_rule(sample: Sample, rule: Rule) -> bool:
    lower_idx = maybe_first_idx(sample, rule.lower)
    upper_idx = maybe_first_idx(sample, rule.upper)
    if lower_idx is not None and upper_idx is not None:
        if lower_idx <= upper_idx:
            passes = True
        else:
            passes = False
    else:
        passes = True
    return passes


T = TypeVar("T")


def first_idx(a_list: list[T], match: T) -> int:
    try:
        return next(idx for (idx, val) in enumerate(a_list) if val == match)
    except StopIteration:
        raise StopIteration(f"Could not find '{match}' in input: {a_list}")


def maybe_first_idx(a_list: list[T], match: T) -> int | None:
    return next((idx for (idx, val) in enumerate(a_list) if val == match), None)


def parse(raw_input: list[str]) -> ParsedInput:
    split_idx = first_idx(raw_input, match="\n")
    rules = [parse_rule(line) for line in raw_input[:split_idx]]
    samples = [parse_sample(line) for line in raw_input[split_idx + 1 :]]
    return ParsedInput(rules=rules, samples=samples)


def parse_rule(raw_line: str) -> Rule:
    rule_parts = raw_line.split("|")
    assert len(rule_parts) == 2, f"Should be two parts to each rule, got: {rule_parts}"
    return Rule(lower=int(rule_parts[0]), upper=int(rule_parts[1]))


def parse_sample(raw_line: str) -> Sample:
    return [int(a) for a in raw_line.strip().split(",")]


if __name__ == "__main__":
    main()
