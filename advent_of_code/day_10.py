import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from advent_of_code.utils import (
    read_input_stripped,
    solve,
    test,
    combine_sets,
    parse_args,
    configure_logging,
)

Grid = list[list[int]]


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Direction(Enum):
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)


def main():
    args = parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_10.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day_10_sample.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=36)
    solve(inputs, part_1, "Part 1")
    test(sample_inputs, part_2, "Part 2 test", expected=81)
    solve(inputs, part_2, "Part 2")


def parse_inputs(inputs: list[str]) -> Grid:
    return [[int(char) for char in line] for line in inputs]


def value_at(grid: Grid, coord: Coord) -> int:
    return grid[coord.y][coord.x]


def in_grid(grid: Grid, coord: Coord) -> bool:
    return 0 <= coord.x < len(grid[0]) and 0 <= coord.y < len(grid)


def coords_with(grid: Grid, value: int) -> set[Coord]:
    return {Coord(x, y) for y, row in enumerate(grid) for x, v in enumerate(row) if v == value}


def find_paths_down_from(current: Coord, grid: Grid) -> set[tuple[Coord, ...]]:
    if value_at(grid, current) == 0:
        return {(current,)}
    paths = set()
    for direction in Direction:
        if next_coord := get_next_valid_coord(current, direction, grid):
            paths |= {(*p, current) for p in find_paths_down_from(next_coord, grid)}
    return paths


def get_next_valid_coord(current: Coord, direction: Direction, grid: Grid) -> Coord | None:
    dx, dy = direction.value
    next_coord = Coord(current.x + dx, current.y + dy)
    if in_grid(grid, next_coord) and value_at(grid, next_coord) == value_at(grid, current) - 1:
        return next_coord
    else:
        return None


def paths_in_grid(grid):
    peaks = coords_with(grid, value=9)
    return combine_sets(find_paths_down_from(peak, grid) for peak in peaks)


def part_1(grid: Grid) -> int:
    paths = paths_in_grid(grid)
    paths_with_unique_start_and_end = {(p[0], p[-1]) for p in paths}
    return len(paths_with_unique_start_and_end)


def part_2(grid: Grid) -> int:
    return len(paths_in_grid(grid))


def print_paths(paths: set[tuple[Coord, ...]], grid: Grid) -> None:
    pts_in_paths = {coord for path in paths for coord in path}
    for y, line in enumerate(grid):
        to_print = [str(val) if Coord(x, y) in pts_in_paths else "." for x, val in enumerate(line)]
        print("".join(to_print))


if __name__ == "__main__":
    main()
