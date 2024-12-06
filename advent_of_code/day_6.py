from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from advent_of_code.utils import read_input, solve, test, replace_item_in_list, idx_of_first_match


class GridValue(Enum):
    OBSTACLE = 0
    GUARD_NOT_BEEN = 1
    GUARD_BEEN = 2

class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

def turn_right(current: Direction) -> Direction:
    return Direction((current.value + 1) % 4)

def parse_grid_value(char: str) -> GridValue:
    match char:
        case "#":
            return GridValue.OBSTACLE
        case ".":
            return GridValue.GUARD_NOT_BEEN
        case "^":
            # Guard has been to the starting position
            return GridValue.GUARD_BEEN
        case _:
            raise ValueError(f"Got unexpected input item {char}")

Grid = list[list[GridValue]]

@dataclass
class Position:
    row_idx: int
    col_idx: int

@dataclass
class Area:
    grid: Grid
    guard_position: Position
    guard_direction: Direction

    @property
    def value_at(self, position: Position) -> GridValue:
        return self.grid[position.row_idx][position.col_idx]
    @property
    def row(self, idx: int) -> list[GridValue]:
        return self.grid[idx]

    @property
    def col(self, idx: int) -> list[GridValue]:
        return [self.grid[row][idx] for row in range(len(self.grid))]

    @property
    def guard_there(self) -> bool:
        return 0 <= self.guard_position.row_idx <= len(self.grid) and 0 <= self.guard_position.col_idx <= len(self.grid[0])

def update_area_row(area: Area, row_idx: int, new_row: list[GridValue], new_guard_position: Position, new_guard_dir: Direction) -> Area:
    new_grid = area.grid
    new_grid.pop(row_idx)
    new_grid.insert(row_idx, new_row)
    return Area(grid=new_grid, guard_position=new_guard_position, guard_direction=new_guard_dir)

def update_area_col(area: Area, col_idx: int, new_col: list[GridValue], new_guard_position: Position, new_guard_dir: Direction) -> Area:
    new_grid = [replace_item_in_list(row, col_idx, new_col[row_idx]) for (row_idx, row) in enumerate(area.grid)]
    return Area(grid=new_grid, guard_position=new_guard_position, guard_direction=new_guard_dir)

def next_obstacle(area: Area) -> Position:
    

def parse_area(inputs: list[str]) -> Area:
    grid = [[parse_grid_value(char) for char in line] for line in inputs]
    guard_row = next(i for (i,row) in enumerate(grid) if GridValue.GUARD_BEEN in row)
    guard_col = idx_of_first_match(grid[guard_row], GridValue.GUARD_BEEN)
    return Area(grid, guard_position=Position(guard_row, guard_col))

def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = read_input("day_6.txt")
    sample_inputs = read_input("day_6_sample.txt")
    test(sample_inputs, part_1, "Part 1 test", expected=41)
    solve(inputs, part_1, "Part 1")


def part_1(inputs: list[str]) -> int:
    area = parse_area(inputs)
    while area.guard_there:
        match area.guard_direction:
            case Direction.N:
                new_col = area.col[]
                area = update_area_col(area, area.guard_position.row_idx, )




if __name__ == "__main__":
    main()
