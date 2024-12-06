import copy
from pathlib import Path
from typing import Callable, TypeVar
from advent_of_code import ASSETS_DIR

TEST_SAMPELES_PART_1 = [
    ([42, 44, 47, 49, 51, 52, 54, 52], False),
    ([7, 6, 4, 2, 1], True),
    ([1, 2, 7, 8, 9], False),
    ([9, 7, 6, 2, 1], False),
    ([1, 3, 2, 4, 5], False),
    ([8, 6, 4, 4, 1], False),
    ([1, 3, 6, 7, 9], True),
]

TEST_SAMPELES_PART_2 = [
    ([42, 44, 47, 49, 51, 52, 54, 52], True),
    ([7, 6, 4, 2, 1], True),
    ([1, 2, 7, 8, 9], False),
    ([9, 7, 6, 2, 1], False),
    ([1, 3, 2, 4, 5], True),
    ([8, 6, 4, 4, 1], True),
    ([1, 3, 6, 7, 9], True),
]


def main():
    print(f"Running script {Path(__file__).name}...")
    file = ASSETS_DIR / "day_2.txt"
    with open(file) as f:
        input_reports = [[int(num) for num in line.split()] for line in f.readlines()]
    part_1(input_reports)
    part_2(input_reports)


def part_2(input_reports: list[list[int]]):
    for item in TEST_SAMPELES_PART_2:
        assert part_2_report_check_safe(item[0]) == item[1], f"{item[0]} should be {item[1]}"
    print("Part 2 test samples all checked correctly...")
    safe_reports = list(filter(part_2_report_check_safe, input_reports))
    print(f"Number reports safe: {len(safe_reports)}")
    assert len(safe_reports) == 349  # Add after puzzle solved for safe refactor


def part_1(input_reports: list[list[int]]):
    for item in TEST_SAMPELES_PART_1:
        assert part_1_report_check_safe(item[0]) == item[1]
    print("Part 1 test samples all checked correctly...")
    safe_reports = list(filter(part_1_report_check_safe, input_reports))
    print(f"Number reports safe: {len(safe_reports)}")
    assert len(safe_reports) == 282  # Add after puzzle solved for safe refactor


def part_2_report_check_safe(report: list[int]) -> bool:
    return check_with_error_allowed(report, gradually_decreasing) or check_with_error_allowed(
        report, gradually_increasing
    )


def check_with_error_allowed(
    report: list[int],
    checker: Callable[[int, int], bool],
    allowed_errors: int = 1,
    error_count: int = 0,
) -> bool:
    for idx, val in enumerate(report[:-1]):
        if not checker(val, report[idx + 1]):
            if error_count >= allowed_errors:
                return False
            return check_with_error_allowed(
                copy_list_deleting_idx(report, idx), checker, error_count=error_count + 1
            ) or check_with_error_allowed(
                copy_list_deleting_idx(report, idx + 1), checker, error_count=error_count + 1
            )
    return True


T = TypeVar("T")


def copy_list_deleting_idx(input: list[T], idx_to_remove: int) -> list[T]:
    copy_ = copy.deepcopy(input)
    del copy_[idx_to_remove]
    return copy_


def gradually_decreasing(a: int, b: int) -> bool:
    return -3 <= (b - a) <= -1


def gradually_increasing(a: int, b: int) -> bool:
    return 1 <= (b - a) <= 3


def part_1_report_check_safe(report: list[int]) -> bool:
    comparison_zip = list(zip(report[:-1], report[1:], strict=True))
    return all(gradually_decreasing(a, b) for (a, b) in comparison_zip) or all(
        gradually_increasing(a, b) for (a, b) in comparison_zip
    )


if __name__ == "__main__":
    main()
