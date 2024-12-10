import itertools
from dataclasses import dataclass
from enum import Enum, member
from operator import mul, add
from pathlib import Path
from typing import Iterator, TypeVar

from more_itertools import distinct_permutations

from advent_of_code.utils import read_input, solve, flatten


@dataclass(frozen=True)
class Equation:
    target: int
    parameters: list[int]


def concat(a: int, b: int) -> int:
    return int(f"{a}{b}")


class Op(Enum):
    MULTIPLY = mul
    ADD = add
    CONCAT = member(concat)


def parse_inputs(inputs: list[str]) -> list[Equation]:
    return [parse_line(li) for li in inputs]


def parse_line(line: str) -> Equation:
    target = int(line.split(":")[0])
    params = [int(num) for num in line.split(":")[1].split()]
    return Equation(target, params)


def equation_solvable_brute_force(eq: Equation, allowed: list[Op]) -> bool:
    return any(
        calculate(eq.parameters, ops) == eq.target
        for ops in combinations(allowed, len(eq.parameters) - 1)
    )


def calculate(params: list[int], operators: tuple[Op, ...]) -> int:
    ans = params[0]
    for param, op in zip(params[1:], operators, strict=True):
        ans = op.value(ans, param)
    return ans


T = TypeVar("T")


def combinations(items: list[T], num_operators: int) -> Iterator[tuple[T, ...]]:
    combs = itertools.combinations_with_replacement(items, num_operators)
    return flatten([distinct_permutations(c) for c in combs])  # type: ignore


def equation_solvable(eq: Equation, allowed_ops: list[Op]) -> bool:
    all_but_last, last_param = eq.parameters[:-1], eq.parameters[-1]
    if len(all_but_last) == 0:
        return last_param == eq.target
    if Op.ADD in allowed_ops and last_param <= eq.target:
        # Check if rest of the eqn works with ADD but also continue checking the other ops
        # i.e. don't do `return equation_solvable(...)`
        if equation_solvable(Equation(eq.target - last_param, all_but_last), allowed_ops):
            return True
    if Op.MULTIPLY in allowed_ops and eq.target % last_param == 0:
        if equation_solvable(Equation(int(eq.target / last_param), all_but_last), allowed_ops):
            return True
    if Op.CONCAT in allowed_ops and is_match_by_final_digits(eq.target, last_param):
        new_target = int(str(eq.target)[: -len(str(last_param))])
        if equation_solvable(Equation(new_target, all_but_last), allowed_ops):
            return True
    return False


def is_match_by_final_digits(to_check: int, query: int) -> bool:
    checker_last_digits = int(str(to_check)[-len(str(query)) :])
    return checker_last_digits == query


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input("day_7.txt"))
    print(f"Max params = {max(len(e.parameters) for e in inputs)}")
    solve(inputs, part_1, "Part 1")
    solve(inputs, part_2_fast, "Part 2")


def part_1(inputs: list[Equation]) -> int:
    solvable = [eq for eq in inputs if equation_solvable(eq, [Op.MULTIPLY, Op.ADD])]
    return sum(eq.target for eq in solvable)


def part_2_brute_force(inputs: list[Equation]) -> int:
    solvable = [
        eq for eq in inputs if equation_solvable_brute_force(eq, [Op.MULTIPLY, Op.ADD, Op.CONCAT])
    ]
    return sum(eq.target for eq in solvable)


def part_2_fast(inputs: list[Equation]) -> int:
    solvable = [eq for eq in inputs if equation_solvable(eq, [Op.MULTIPLY, Op.ADD, Op.CONCAT])]
    return sum(eq.target for eq in solvable)


if __name__ == "__main__":
    main()
