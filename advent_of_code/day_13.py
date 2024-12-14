from dataclasses import dataclass
from pathlib import Path
import re

from advent_of_code.utils import read_input_stripped, solve, test, Vector


@dataclass(frozen=True)
class Button:
    vector: Vector
    cost: int


@dataclass(frozen=True)
class ClawMachine:
    a: Button
    b: Button
    prize: Vector


def is_positive_int(num: float) -> bool:
    return num >= 0 and int(num) == num


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_13.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day_13_sample.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=480)
    solve(inputs, part_1, "Part 1")
    solve(inputs, part_2, "Part 2")


def parse_inputs(inputs: list[str]) -> list[ClawMachine]:
    machines = []
    for i, line in enumerate(inputs):
        match i % 4:
            case 0:
                button_a = parse_button(line, cost=3)
            case 1:
                button_b = parse_button(line, cost=1)
            case 2:
                prize = parse_prize(line)
                machines.append(ClawMachine(button_a, button_b, prize))  # type: ignore
            case 3:
                pass
    return machines


def parse_button(line: str, cost: int) -> Button:
    try:
        x = re.search(r"X\+(\d+)", line).group(1)  # type: ignore
        y = re.search(r"Y\+(\d+)", line).group(1)  # type: ignore
    except AttributeError:
        raise ValueError(f"Could not parse {line=} into button")
    return Button(Vector(x=int(x), y=int(y)), cost)


def parse_prize(line: str) -> Vector:
    try:
        x = re.search(r"X\=(\d+)", line).group(1)  # type: ignore
        y = re.search(r"Y\=(\d+)", line).group(1)  # type: ignore
    except AttributeError:
        raise ValueError(f"Could not parse {line=} into prize")
    return Vector(x=int(x), y=int(y))


def part_1(machines: list[ClawMachine]) -> int:
    return sum(c for c in [cost(m) for m in machines] if c is not None)


def cost(machine: ClawMachine) -> int | None:
    det_a_b = machine.a.vector.determinant(machine.b.vector)
    det_b_prize = machine.b.vector.determinant(machine.prize)
    # if det(x, y) == 0 then x and y are in the same line
    if det_a_b == 0 and det_b_prize == 0:
        b_movements = machine.prize.magnitude / machine.b.vector.magnitude
        if is_positive_int(b_movements):
            return int(b_movements)
    else:
        # If p = n*a + m*b, where p, a and b are vectors, then
        # p1 = n*a1 + m*b1  and  p2 = n*a2 + m*b2
        # Rearranging and using determinants, n = det(p,b)/det(a,b), (m similar)
        # Determinant(a,b) is area of parallelogram formed by a and b
        a_movements = machine.prize.determinant(machine.b.vector) / det_a_b
        b_movements = machine.a.vector.determinant(machine.prize) / det_a_b
        if is_positive_int(a_movements) and is_positive_int(b_movements):
            return int(b_movements * machine.b.cost + a_movements * machine.a.cost)
    return None


def part_2(original_machines: list[ClawMachine]) -> int:
    part_2_machines = [
        ClawMachine(m.a, m.b, m.prize + Vector(x=10000000000000, y=10000000000000))
        for m in original_machines
    ]
    return sum(c for c in [cost(m) for m in part_2_machines] if c is not None)


if __name__ == "__main__":
    main()
