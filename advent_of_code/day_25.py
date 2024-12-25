import logging
from dataclasses import dataclass
from pathlib import Path

from advent_of_code.utils import (
    read_input_stripped,
    solve,
    test,
    parse_args,
    configure_logging,
    idx_of_first_match,
)

Pins = tuple[int, int, int, int, int]


@dataclass
class Lock:
    pin_heights: Pins


@dataclass
class Key:
    pin_heights: Pins


@dataclass
class ParsedInputs:
    keys: list[Key]
    locks: list[Lock]


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    sample_inputs = parse_inputs(read_input_stripped("day_25_sample.txt"))
    inputs = parse_inputs(read_input_stripped("day_25.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=3)
    solve(inputs, part_1, "Part 1")


def parse_inputs(inputs: list[str]) -> ParsedInputs:
    locks, keys = [], []
    for idx in range(0, len(inputs), 8):
        pins_raw = inputs[idx : idx + 7]
        if inputs[idx] == "#" * 5:
            locks.append(Lock(parse_pins(pins_raw)))
        elif inputs[idx] == "." * 5:
            keys.append(Key(parse_pins(list(reversed(pins_raw)))))
        else:
            raise ValueError(f"Unexpected line: {inputs[idx]}")
    return ParsedInputs(locks=locks, keys=keys)


def parse_pins(pins_raw: list[str]) -> Pins:
    return tuple([parse_pin(i, pins_raw) for i in range(5)])  # type: ignore


def parse_pin(idx: int, pins_raw: list[str]) -> int:
    pin = [line[idx] for line in pins_raw]
    return idx_of_first_match(pin, match=".") - 1


def has_non_overlapping_fit(key: Key, lock: Lock) -> bool:
    return all(k + lo <= 5 for k, lo in zip(key.pin_heights, lock.pin_heights, strict=True))


def part_1(inputs: ParsedInputs) -> int:
    logging.debug(f"Full inputs: {inputs}")
    non_overlapping_fits = 0
    for key in inputs.keys:
        for lock in inputs.locks:
            non_overlapping_fits += int(has_non_overlapping_fit(key, lock))
    return non_overlapping_fits


if __name__ == "__main__":
    main()
