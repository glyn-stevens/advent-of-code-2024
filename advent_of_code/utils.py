from dataclasses import dataclass
from typing import Callable, TypeVar, Iterable

from advent_of_code import ASSETS_DIR

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
        return f"({self.x}, {self.y})"
