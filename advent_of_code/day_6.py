import copy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from advent_of_code.utils import (
    read_input,
    solve,
    test,
    idx_of_first_match,
)


class GridValue(Enum):
    OBSTACLE = "#"
    GUARD_NOT_BEEN = "."
    GUARD_BEEN = "X"


class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


GUARD_CHAR = {Direction.N: "^", Direction.E: ">", Direction.S: "v", Direction.W: "<"}


def turn_right(current: Direction) -> Direction:
    return Direction((current.value + 1) % 4)


def parse_grid_value(char: str) -> GridValue:
    match char:
        case "#":
            return GridValue.OBSTACLE
        case ".":
            return GridValue.GUARD_NOT_BEEN
        case "^":
            # Guard has been to the starting position, and is the only position they've been
            return GridValue.GUARD_BEEN
        case _:
            raise ValueError(f"Got unexpected input item: '{char}'")


@dataclass(frozen=True)
class Position:
    row_idx: int
    col_idx: int


class GoneBeyondGridError(ValueError):
    pass


class Area:
    grid: list[list[GridValue]]
    guard_position: Position
    guard_direction: Direction

    def __init__(
        self, grid: list[list[GridValue]], guard_position: Position, guard_direction: Direction
    ):
        self.grid = grid
        self.guard_position = guard_position
        self.guard_direction = guard_direction

    def spaces_at_value(self, val: GridValue) -> int:
        return sum(line.count(val) for line in self.grid)

    @property
    def next_space_idx(self) -> Position:
        gp = self.guard_position
        match self.guard_direction:
            case Direction.N:
                next_idx = Position(gp.row_idx - 1, gp.col_idx)
            case Direction.E:
                next_idx = Position(gp.row_idx, gp.col_idx + 1)
            case Direction.S:
                next_idx = Position(gp.row_idx + 1, gp.col_idx)
            case Direction.W:
                next_idx = Position(gp.row_idx, gp.col_idx - 1)
            case _:
                raise ValueError(f"Invalid direction: {self.guard_direction}")
        # print(f"{gp=}, {next_idx}")
        return next_idx

    def move(self):
        next_space_idx = self.next_space_idx
        self.set_grid_idx(self.guard_position, GridValue.GUARD_BEEN)
        if self.position_valid(next_space_idx):
            if self.get_grid_value(next_space_idx) == GridValue.OBSTACLE:
                # print("Turning")
                self.set_guard_direction(turn_right(self.guard_direction))
            else:
                # print(f"Moving guard to {next_space_idx}")
                self.set_guard_position(next_space_idx)
        else:
            raise GoneBeyondGridError("Guard gone beyond grid")

    def set_guard_direction(self, new_dir: Direction):
        self.guard_direction = new_dir

    def set_guard_position(self, new_pos: Position):
        self.guard_position = new_pos

    def set_grid_idx(self, position: Position, new_val: GridValue):
        assert self.position_valid(position), f"{position = } is not in the grid"
        self.grid[position.row_idx][position.col_idx] = new_val

    def get_grid_value(self, position: Position) -> GridValue | None:
        if not self.position_valid(position):
            return None
        return self.grid[position.row_idx][position.col_idx]

    def guard_there(self) -> bool:
        return 0 <= self.guard_position.row_idx <= len(
            self.grid
        ) and 0 <= self.guard_position.col_idx <= len(self.grid[0])

    def position_valid(self, position: Position) -> bool:
        return (
            0 <= position.row_idx <= len(self.grid) - 1
            and 0 <= position.col_idx <= len(self.grid[0]) - 1
        )

    def print(self):
        print(f"Guard pos = {self.guard_position}, Grid = \n")
        for i, line in enumerate(self.grid):
            if i == self.guard_position.row_idx:
                guard = GUARD_CHAR[self.guard_direction]
                print(
                    f"{line_to_str(line[:self.guard_position.col_idx])}{guard}{line_to_str(line[self.guard_position.col_idx + 1:])}"
                )
            else:
                print(line_to_str(line))


def line_to_str(line: list[GridValue]) -> str:
    return "".join([v.value for v in line])


def parse_area(inputs: list[str]) -> Area:
    grid = [[parse_grid_value(char) for char in line.strip()] for line in inputs]
    guard_row = next(i for (i, row) in enumerate(grid) if GridValue.GUARD_BEEN in row)
    guard_col = idx_of_first_match(grid[guard_row], GridValue.GUARD_BEEN)
    # Guard always starts pointing N
    return Area(grid, guard_position=Position(guard_row, guard_col), guard_direction=Direction.N)


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = read_input("day_6.txt")
    sample_inputs = read_input("day_6_sample.txt")
    # test(sample_inputs, part_1, "Part 1 test", expected=41)
    solve(inputs, part_1, "Part 1")
    test(sample_inputs, part_2, "Part 2 test", expected=6)
    solve(inputs, part_2, "Part 2")


def part_1(inputs: list[str]) -> int:
    area = parse_area(inputs)
    while True:
        try:
            area.move()
        except GoneBeyondGridError:
            break
    return area.spaces_at_value(GridValue.GUARD_BEEN)


def part_2(inputs: list[str]) -> int:
    area = parse_area(inputs)
    possible_blockade_positions: set[Position] = set()
    sexy = True
    while True:
        potential_blockade_pos = area.next_space_idx
        if not area.position_valid(potential_blockade_pos) or area.get_grid_value(
            potential_blockade_pos
        ) in [GridValue.OBSTACLE, GridValue.GUARD_BEEN]:
            # Can't put it where guard has been, and doesn't change outcome if space is already an obstacle
            print(f"Not trying blockade in {potential_blockade_pos}")
        else:
            # Try putting an obstacle immediately ahead of guard
            test_area = copy.deepcopy(area)
            test_area.set_grid_idx(potential_blockade_pos, GridValue.OBSTACLE)
            test_area_guard_posns: set[tuple[Position, Direction]] = set()
            while True:
                try:
                    # print(f"{test_area.guard_position}")
                    test_area.move()
                    if (
                        test_area.guard_position,
                        test_area.guard_direction,
                    ) in test_area_guard_posns:
                        print("Found blockade posn...")
                        possible_blockade_positions.add(potential_blockade_pos)
                        break
                    else:
                        test_area_guard_posns.add(
                            (
                                copy.deepcopy(test_area.guard_position),
                                copy.deepcopy(test_area.guard_direction),
                            )
                        )
                except GoneBeyondGridError:
                    break
        try:
            area.move()
            # print(f"{area.guard_position=}")
        except GoneBeyondGridError:
            break
    if sexy:
        area.print()
    return len(possible_blockade_positions)


if __name__ == "__main__":
    main()
