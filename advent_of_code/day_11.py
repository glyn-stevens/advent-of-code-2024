from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_11.txt"))
    sample_inputs = [125, 17]
    test(sample_inputs, part_1, "Part 1 test", expected=55312)
    solve(inputs, part_1, "Part 1")
    test(sample_inputs, part_2, "Part 2 test", expected=55312)
    solve(inputs, part_2, "Part 2")

def parse_inputs(ins: list[str]) -> list[int]:
    return [int(num) for num in ins[0].split()]

def blink(num: int) -> tuple[int, ...]:
    if num == 0:
        return (1,)
    num_str = str(num)
    if len(num_str) % 2 == 0:
        split_idx = int(len(num_str) / 2)
        return (int(num_str[:split_idx]), int(num_str[split_idx:]))
    return (num * 2024,)

def blink_list(inputs: list[int]) -> list[int]:
    return [x for num in inputs for x in blink(num)]

def part_1(inputs: list[int]) -> int:
    ongoing = inputs
    for i in range(25):
        ongoing = blink_list(ongoing)
    return len(ongoing)

def part_2(inputs: list[int]) -> int:
    ongoing = inputs
    for i in range(75):
        if i % 5 == 0:
            print(f"At cycle {i}")
        ongoing = blink_list(ongoing)
    return len(ongoing)


if __name__ == "__main__":
    main()
