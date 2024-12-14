import math
from dataclasses import dataclass
from math import floor, ceil
from pathlib import Path
import re

from advent_of_code.utils import read_input_stripped, solve, test, Vector, Coord, in_area


@dataclass(frozen=True)
class Robot:
    position: Coord
    velocity: Vector


@dataclass(frozen=True)
class Area:
    robots: list[Robot]
    grid_size: Coord


Rectangle = tuple[Coord, Coord]


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = Area(parse_inputs(read_input_stripped("day_14.txt")), Coord(101, 103))
    sample_inputs = Area(parse_inputs(read_input_stripped("day_14_sample.txt")), Coord(11, 7))
    test(sample_inputs, part_1, "Part 1 test", expected=12)
    solve(inputs, part_1, "Part 1")
    # solve(inputs, part_2, "Part 2")


def parse_inputs(inputs: list[str]) -> list[Robot]:
    return [parse_robot(line) for line in inputs]


def parse_robot(line: str) -> Robot:
    try:
        px = re.search(r"p=(-?\d+)", line).group(1)  # type: ignore
        py = re.search(r"p=-?\d+,(-?\d+)", line).group(1)  # type: ignore
        vx = re.search(r"v=(-?\d+)", line).group(1)  # type: ignore
        vy = re.search(r"v=-?\d+,(-?\d+)", line).group(1)  # type: ignore
    except AttributeError:
        raise ValueError(f"Could not parse {line=} into robot")
    return Robot(Coord(int(px), int(py)), Vector(int(vx), int(vy)))


def quadrants(grid_size: Coord) -> tuple[Rectangle, Rectangle, Rectangle, Rectangle]:
    x = grid_size.x
    y = grid_size.y
    a = (Coord(0, 0), Coord(floor(x / 2) - 1, floor(y / 2) - 1))
    b = (Coord(ceil(x / 2), 0), Coord(x, floor(y / 2) - 1))
    c = (Coord(0, ceil(y / 2)), Coord(floor(x / 2) - 1, y))
    d = (Coord(ceil(x / 2), ceil(y / 2)), Coord(x, y))
    return (a, b, c, d)


def move(position: Coord, vector: Vector, grid_size: Coord) -> Coord:
    return Coord((position.x + vector.x) % grid_size.x, (position.y + vector.y) % grid_size.y)


def part_1(inputs: Area) -> int:
    seconds = 100
    robot_end_positions = [
        move(r.position, r.velocity * seconds, inputs.grid_size) for r in inputs.robots
    ]
    scores = []
    for quadrant in quadrants(inputs.grid_size):
        print(f"{quadrant=}")
        score = len([r for r in robot_end_positions if in_area(r, quadrant[0], quadrant[1])])
        print(f"{score=}")
        scores.append(score)
    return math.prod(scores)


def part_2(inputs: Area) -> int:
    return 0


if __name__ == "__main__":
    main()
