import logging
import math
from dataclasses import dataclass
from pathlib import Path
import re
from advent_of_code.utils import (
    read_input_stripped,
    solve,
    test,
    Vector,
    Coord,
    in_area_inclusive,
    configure_logging,
    parse_args,
)


@dataclass(frozen=True)
class Robot:
    position: Coord
    velocity: Vector


@dataclass(frozen=True)
class Area:
    robots: list[Robot]
    grid_size: Coord

    def __repr__(self):
        def char_at(coord: Coord) -> str:
            robos = len([r for r in self.robots if r.position == coord])
            return str(robos) if robos > 0 else "."

        def line_repr(y: int) -> str:
            return "".join(char_at(Coord(x, y)) for x in range(self.grid_size.x + 1))

        return "\n".join(line_repr(y) for y in range(self.grid_size.y + 1))


Rectangle = tuple[Coord, Coord]


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    inputs = Area(parse_inputs(read_input_stripped("day_14.txt")), Coord(100, 102))
    sample_inputs = Area(parse_inputs(read_input_stripped("day_14_sample.txt")), Coord(10, 6))
    test(sample_inputs, part_1, "Part 1 test", expected=12)
    # solve(inputs, part_1, "Part 1")
    solve(inputs, part_2, "Part 2")


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


def quadrants_with_gap(grid_size: Coord) -> list[Rectangle]:
    x = grid_size.x
    y = grid_size.y
    a = (Coord(0, 0), Coord(x // 2 - 1, y // 2 - 1))
    b = (Coord(x // 2 + 1, 0), Coord(x, y // 2 - 1))
    c = (Coord(0, y // 2 + 1), Coord(x // 2 - 1, y))
    d = (Coord(x // 2 + 1, y // 2 + 1), Coord(x, y))
    return [a, b, c, d]


def divide_grid(grid_size: Coord, num_rows_cols: int) -> list[Rectangle]:
    dx = grid_size.x // num_rows_cols
    dy = grid_size.y // num_rows_cols
    return [
        (Coord(dx * x_scale, dy * y_scale), Coord(dx * (x_scale + 1), dy * (y_scale + 1)))
        for x_scale in range(num_rows_cols)
        for y_scale in range(num_rows_cols)
    ]


def move(position: Coord, vector: Vector, grid_size: Coord) -> Coord:
    return Coord(
        (position.x + vector.x) % (grid_size.x + 1), (position.y + vector.y) % (grid_size.y + 1)
    )


def get_danger_score(robots: list[Coord], sub_areas: list[Rectangle]) -> int:
    scores = [len([r for r in robots if in_area_inclusive(r, a[0], a[1])]) for a in sub_areas]
    return math.prod(scores)


def part_1(inputs: Area) -> int:
    seconds = 100
    robot_end_positions = [
        move(r.position, r.velocity * seconds, inputs.grid_size) for r in inputs.robots
    ]
    return get_danger_score(robot_end_positions, quadrants_with_gap(inputs.grid_size))


def part_2(inputs: Area) -> int:
    start = 6200  # Start later now that we've solved it
    robots = [
        Robot(move(r.position, r.velocity * start, inputs.grid_size), r.velocity)
        for r in inputs.robots
    ]
    sub_grids = divide_grid(inputs.grid_size, num_rows_cols=3)
    danger_scores = []
    for i in range(start, 10000):
        danger_score = get_danger_score([r.position for r in robots], sub_grids)
        danger_scores.append(danger_score)
        avg_danger = sum(danger_scores) / len(danger_scores)
        if danger_score < avg_danger / 65:
            break
        robots = [
            Robot(move(r.position, r.velocity, inputs.grid_size), r.velocity) for r in robots
        ]
        i += 1
    return i


if __name__ == "__main__":
    main()
