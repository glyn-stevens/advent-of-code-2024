from typing import Callable, TypeVar

from advent_of_code import ASSETS_DIR

T = TypeVar("T")
U = TypeVar("U")
INDENT = "    "


def solve(input: T, solver: Callable[[T], U], description: str, expected: U | None = None) -> U:
    print(f"\n🤞 Solving {description}...")
    output = _solve_with_log(input, solver, description)
    return _check(output, expected) if expected else output


def test(
    inputs: list[T], solver: Callable[[T], U], description: str, expected: list[U]
) -> list[U]:
    print(f"\n🧪 Running tests for {description}...")
    return [
        _check(_solve_with_log(input, solver, f"{description} - test {i}"), expect)
        for i, (input, expect) in enumerate(zip(inputs, expected, strict=True))
    ]


def _check(output: T, expected: T) -> T:
    assert output == expected, f"\n{INDENT}❌ Checks failed\nGot: {output}\nExpected: {expected}"
    print(f"{INDENT}✅ Checks passed")
    return output


def _solve_with_log(input: T, solver: Callable[[T], U], description: str) -> U:
    print(f"{INDENT}Input for {description} is '{str(input)[:40]}...'")
    output = solver(input)
    print(f"{INDENT}👉 Solution: {output}")
    return output


def read_input(day: int) -> list[str]:
    with open(ASSETS_DIR / f"day_{day}.txt") as f:
        return list(f.readlines())
