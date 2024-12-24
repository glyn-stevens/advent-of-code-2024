from __future__ import annotations
import logging
from dataclasses import dataclass
from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test, parse_args, configure_logging


Towel = str


@dataclass(frozen=True)
class ParsedInputs:
    components: list[Towel]
    targets: list[Towel]


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_19.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day_19_sample.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=6)
    solve(inputs, part_1, "Part 1")
    test(sample_inputs, part_2, "Part 2 test", expected=16)
    solve(inputs, part_2, "Part 2")


def parse_inputs(inputs: list[str]) -> ParsedInputs:
    components = [Towel(towel.strip()) for towel in inputs[0].split(",")]
    targets = [Towel(i) for i in inputs[2:]]
    return ParsedInputs(components, targets)


def get_number_combinations(
    target: Towel, components: list[Towel], targets_tested: dict[str, int]
) -> dict[str, int]:
    number_combinations = 0
    if target in targets_tested:
        return targets_tested
    for component in components:
        if target == component:
            number_combinations += 1
        elif target.startswith(component):
            new_target = target[len(component) :]
            targets_tested = get_number_combinations(new_target, components, targets_tested)
            number_combinations += targets_tested[new_target]
    targets_tested[target] = number_combinations
    return targets_tested


def part_1(inputs: ParsedInputs) -> int:
    possible = [
        max(get_number_combinations(t, inputs.components, dict()).values()) for t in inputs.targets
    ]
    return len([p for p in possible if p > 0])


def part_2(inputs: ParsedInputs) -> int:
    total = 0
    for t in inputs.targets:
        tested = get_number_combinations(t, inputs.components, dict())
        logging.debug(f"For target {t}, tested: {tested}")
        total += max(tested.values())
    return total


if __name__ == "__main__":
    main()
