from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Callable, TypeVar, Iterable

from advent_of_code import ASSETS_DIR
import logging
import argparse
import sys



T = TypeVar("T")
U = TypeVar("U")
INDENT = "    "


def solve(input: T, solver: Callable[[T], U], description: str) -> U:
    print(f"\n🤞 Solving {description}...")
    output = _solve_with_log(input, solver, description)
    return output


def test_multiple(
    inputs: list[T], solver: Callable[[T], U], description: str, expected: list[U]
) -> list[U]:
    print(f"\n🧪 Running tests for {description}...")
    return [
        _check(_solve_with_log(input, solver, f"{description} - test {i}"), expect)
        for i, (input, expect) in enumerate(zip(inputs, expected, strict=True))
    ]


def test(inputs: T, solver: Callable[[T], U], description: str, expected: U) -> U:
    print(f"\n🧪 Running test for {description}...")
    return _check(_solve_with_log(inputs, solver, f"{description} - test"), expected)


def _check(output: T, expected: T) -> T:
    assert output == expected, f"\n{INDENT}❌ Checks failed\nGot: {output}\nExpected: {expected}"
    print(f"{INDENT}✅ Checks passed")
    return output


def _solve_with_log(input: T, solver: Callable[[T], U], description: str) -> U:
    print(f"{INDENT}Input for {description} is '{str(input)[:40]}...'")
    output = solver(input)
    print(f"{INDENT}👉 Solution: {output}")
    return output


def read_input(name: str) -> list[str]:
    with open(ASSETS_DIR / name) as f:
        return list(f.readlines())


def read_input_stripped(name: str) -> list[str]:
    with open(ASSETS_DIR / name) as f:
        return [x.strip() for x in list(f.readlines())]


def idx_of_first_match(a_list: list[T], match: T) -> int:
    try:
        return next(idx for (idx, val) in enumerate(a_list) if val == match)
    except StopIteration:
        raise StopIteration(f"Could not find '{match}' in input: {a_list}")


def maybe_idx_of_first_match(a_list: list[T], match: T) -> int | None:
    return next((idx for (idx, val) in enumerate(a_list) if val == match), None)


def replace_item_in_list(a_list: list[T], idx: int, new_item: T) -> list[T]:
    return a_list[:idx] + [new_item] + a_list[idx + 1 :]


def flatten(list_of_list: list[Iterable[T]]) -> list[T]:
    return [x for inner_list in list_of_list for x in inner_list]


def combine_sets(iterable_of_sets: Iterable[set[T]]) -> set[T]:
    return set().union(*iterable_of_sets)


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __repr__(self):
        return f"C({self.x}, {self.y})"

    def __add__(self, vec: Vector):
        return Coord(self.x + vec.x, self.y + vec.y)

    def __lt__(self, other: Coord):
        return (self.y, self.x) < (other.y, other.x)


def in_grid(a: Coord, grid_size: Coord) -> bool:
    return 0 <= a.x <= grid_size.x and 0 <= a.y <= grid_size.y


def in_area_inclusive(a: Coord, corner_1: Coord, corner_2: Coord) -> bool:
    min_x, max_x = min(corner_1.x, corner_2.x), max(corner_1.x, corner_2.x)
    min_y, max_y = min(corner_1.y, corner_2.y), max(corner_1.y, corner_2.y)
    return min_x <= a.x <= max_x and min_y <= a.y <= max_y


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def determinant(self, v2: Vector) -> float:
        return self.x * v2.y - self.y * v2.x

    def __repr__(self):
        return f"V({self.x}, {self.y})"

    def __sub__(self, other: Vector):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other: Vector):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return Vector(self.x * other, self.y * other)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set log verbosity.")
    parser.add_argument(
        '-v',
        action='count',
        default=0,
        help="Increase verbosity with -v or -vv"
    )
    return parser.parse_args()

def configure_logging(args:  argparse.Namespace) -> None:
    if args.v == 1:
        log_level = logging.INFO
    elif args.v >= 2:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )