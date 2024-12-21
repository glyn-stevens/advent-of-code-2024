import logging
from dataclasses import dataclass
from pathlib import Path

from advent_of_code.utils import (
    read_input,
    solve,
    idx_of_first_match,
    maybe_idx_of_first_match,
    parse_args,
    configure_logging,
)


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
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    inputs = read_input("day_5.txt")
    solve(inputs, part_1, "Part 1")
    solve(inputs, part_2, "Part 2")


def part_1(inputs: list[str]) -> int:
    parsed = parse(inputs)
    passing_samples = [s for s in parsed.samples if sample_passes_rules(s, parsed.rules)]
    middle_values = [s[int(len(s) / 2)] for s in passing_samples]
    return sum(middle_values)


def part_2(inputs: list[str]) -> int:
    parsed = parse(inputs)
    failing_samples = [s for s in parsed.samples if not sample_passes_rules(s, parsed.rules)]
    corrected_sampled = [apply_rules(s, parsed.rules) for s in failing_samples]
    middle_values = [s[int(len(s) / 2)] for s in corrected_sampled]
    return sum(middle_values)


def apply_rules(sample: Sample, rules: list[Rule], recursion_depth: int = 0) -> Sample:
    for r in rules:
        lower_idx = maybe_idx_of_first_match(sample, r.lower)
        upper_idx = maybe_idx_of_first_match(sample, r.upper)
        if lower_idx is None or upper_idx is None or lower_idx <= upper_idx:
            continue
        # Reconstruct sample: move the upper value to position immediately after the lower value
        sample = (
            sample[:upper_idx]
            + sample[upper_idx + 1 : lower_idx + 1]
            + [sample[upper_idx]]
            + sample[lower_idx + 1 :]
        )
    if rules_still_failed := [r for r in rules if not sample_passes_rule(sample, r)]:
        assert recursion_depth < 20, f"Recursing too far... {rules_still_failed=} in {sample=}"
        return apply_rules(sample, rules, recursion_depth=recursion_depth + 1)
    return sample


def sample_passes_rules(sample: Sample, rules: list[Rule]) -> bool:
    return all(sample_passes_rule(sample, r) for r in rules)


def sample_passes_rule(sample: Sample, rule: Rule) -> bool:
    lower_idx = maybe_idx_of_first_match(sample, rule.lower)
    upper_idx = maybe_idx_of_first_match(sample, rule.upper)
    if lower_idx is None or upper_idx is None or lower_idx <= upper_idx:
        return True
    return False


def parse(raw_input: list[str]) -> ParsedInput:
    split_idx = idx_of_first_match(raw_input, match="\n")
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
