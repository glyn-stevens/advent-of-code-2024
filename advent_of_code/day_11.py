from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_11.txt"))
    sample_inputs = [125, 17]
    test(sample_inputs, part_1, "Part 1 test", expected=55312)
    solve(inputs, part_1, "Part 1")
    solve(inputs, part_2, "Part 2")


def parse_inputs(ins: list[str]) -> list[int]:
    return [int(num) for num in ins[0].split()]


def cycle(num: int) -> tuple[int, ...]:
    """Apply one iteration of the rules to a single number (which represents a 'stone' in the story)"""
    if num == 0:
        return (1,)
    num_str = str(num)
    if len(num_str) % 2 == 0:
        split_idx = int(len(num_str) / 2)
        return (int(num_str[:split_idx]), int(num_str[split_idx:]))
    return (num * 2024,)


def cycle_multiple(inputs: list[int]) -> list[int]:
    return [x for num in inputs for x in cycle(num)]


def cycle_with_count(input_values_by_count: dict[int, int]) -> dict[int, int]:
    cycled_values_by_count = dict()
    for value, quantity in input_values_by_count.items():
        for result in cycle(value):
            cycled_values_by_count[result] = quantity + cycled_values_by_count.get(result, 0)
    return cycled_values_by_count


def part_1(values: list[int]) -> int:
    for i in range(25):
        values = cycle_multiple(values)
    return len(values)


def part_2(values: list[int]) -> int:
    values_by_count = {val: values.count(val) for val in values}
    for i in range(75):
        if i == 74:
            print(
                f"At cycle {i}, we're tracking {len(values_by_count)} distinct numbers, and {sum(values_by_count.values())} total numbers"
            )
        values_by_count = cycle_with_count(values_by_count)
    return sum(values_by_count.values())


if __name__ == "__main__":
    main()
