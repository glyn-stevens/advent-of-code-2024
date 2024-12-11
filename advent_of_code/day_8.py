import itertools
import math
from dataclasses import dataclass
from pathlib import Path
from advent_of_code.utils import solve, test, flatten, read_input_stripped


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class Grid:
    max_coord: Position
    antennae: dict[str, list[Position]]


def in_grid(a: Position, grid_size: Position) -> bool:
    return 0 <= a.x <= grid_size.x and 0 <= a.y <= grid_size.y


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_8.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day_8_sample.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=14)
    solve(inputs, part_1, "Part 1")
    test(sample_inputs, part_2, "Part 2 test", expected=34)
    solve(inputs, part_2, "Part 2")


def parse_inputs(inputs: list[str]) -> Grid:
    max_coord = Position(len(inputs[0]) - 1, len(inputs) - 1)
    antennae_types = set(flatten(inputs))  # type: ignore
    antennae_types.discard(".")
    antennae = {t: parse_antennae(t, inputs) for t in antennae_types}
    return Grid(max_coord=max_coord, antennae=antennae)


def parse_antennae(type_: str, ins: list[str]) -> list[Position]:
    return [Position(x, y) for y, row in enumerate(ins) for x, c in enumerate(row) if c == type_]


def part_1(inputs: Grid) -> int:
    antinodes = set()
    for posns in inputs.antennae.values():
        for pair in itertools.combinations(posns, r=2):
            antinodes.update(part_1_antinodes(pair[0], pair[1], inputs.max_coord))
    return len(antinodes)


def part_1_antinodes(a: Position, b: Position, grid_size: Position) -> set[Position]:
    x_dif, y_dif = a.x - b.x, a.y - b.y
    first = Position(a.x + x_dif, a.y + y_dif)
    second = Position(b.x - x_dif, b.y - y_dif)
    return {p for p in [first, second] if in_grid(p, grid_size)}


def part_2(inputs: Grid) -> int:
    antinodes = set()
    for posns in inputs.antennae.values():
        for pair in itertools.combinations(posns, r=2):
            antinodes.update(part_2_antinodes(pair[0], pair[1], inputs.max_coord))
    return len(antinodes)


def part_2_antinodes(a: Position, b: Position, grid_size: Position) -> set[Position]:
    # Find the smallest increment by dividing the x and y gaps between pairs of positions by
    # the greatest common denominator of the x and y gap values.
    x_dif, y_dif = a.x - b.x, a.y - b.y
    great_common_denom = math.gcd(x_dif, y_dif)
    x_increment, y_increment = int(x_dif / great_common_denom), int(y_dif / great_common_denom)

    # Starting at 'a', add antinodes in a line until we reach the edge of the grid
    antinodes = positions_in_line_in_grid(a, grid_size, x_increment, y_increment)
    # Then, starting at 'a' again, add antinodes in the opposite direction (until grid edge)
    antinodes.update(positions_in_line_in_grid(a, grid_size, -x_increment, -y_increment))
    return antinodes


def positions_in_line_in_grid(
    start: Position, grid_size: Position, x_increment: int, y_increment: int
) -> set[Position]:
    antinodes = set()
    for multiplier in range(0, max(grid_size.x, grid_size.y)): # Allow stepping until at least edge of grid
        antinode = Position(start.x - x_increment * multiplier, start.y - y_increment * multiplier)
        if not in_grid(antinode, grid_size):
            break
        antinodes.add(antinode)
    return antinodes


def print_grid(inputs: Grid, antinodes: set[Position]) -> None:
    grid = [["."] * (inputs.max_coord.x + 1) for _ in range(inputs.max_coord.y + 1)]
    for a in antinodes:
        try:
            grid[a.y][a.x] = "#"
        except IndexError:
            print(f"Couldn't set item at posn {a} - not in grid")
    for line in grid:
        print("".join(line))


if __name__ == "__main__":
    main()
