import logging
from collections import defaultdict
from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test, parse_args, configure_logging


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_22.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day_22_sample.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=37327623)
    solve(inputs, part_1, "Part 1")
    solve(inputs, part_2, "Part 2")


def parse_inputs(inputs: list[str]) -> list[int]:
    return [int(line) for line in inputs]


def next_secret_number(current: int) -> int:
    step_1 = ((current * 64) ^ current) % 16777216
    step_2 = ((step_1 // 32) ^ step_1) % 16777216
    step_3 = ((step_2 * 2048) ^ step_2) % 16777216
    return step_3


def n_secret_numbers(current: int, n: int) -> list[int]:
    return [current] + [current := next_secret_number(current) for _ in range(n)]


PriceChanges = tuple[int, int, int, int]


def map_cost_to_price_changes(costs: list[int]) -> dict[PriceChanges, int]:
    def price_dif(idx: int) -> int:
        return costs[idx] - costs[idx - 1]

    mapping: dict[PriceChanges, int] = {}
    for idx in range(4, len(costs)):
        price_changes = (
            price_dif(idx - 3),
            price_dif(idx - 2),
            price_dif(idx - 1),
            price_dif(idx),
        )
        if price_changes not in mapping.keys():
            mapping[price_changes] = costs[idx]
    return mapping


def part_1(inputs: list[int]) -> int:
    return sum(n_secret_numbers(num, 2000)[-1] for num in inputs)


def part_2(inputs: list[int]) -> int:
    # Cost is equal to the final digit in the secret number
    all_costs = [[n % 10 for n in n_secret_numbers(num, n=2000)] for num in inputs]

    all_price_changes_by_cost = [map_cost_to_price_changes(costs) for costs in all_costs]
    price_changes_by_occurrences: dict[PriceChanges, int] = defaultdict(int)
    for price_change_by_cost in all_price_changes_by_cost:
        for changes in price_change_by_cost.keys():
            price_changes_by_occurrences[changes] += 1

    highest_total_cost_so_far = 2000  # Initialise value high now puzzle is solved
    for price_changes, occurrences in price_changes_by_occurrences.items():
        if occurrences * 9 <= highest_total_cost_so_far:
            # No way the highest cost can be beaten as highest individual cost is 9
            continue
        total_cost = sum(cost.get(price_changes, 0) for cost in all_price_changes_by_cost)
        highest_total_cost_so_far = max(total_cost, highest_total_cost_so_far)
    return highest_total_cost_so_far


if __name__ == "__main__":
    main()
