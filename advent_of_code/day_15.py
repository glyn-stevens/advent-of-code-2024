import copy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable

import curses
import time
from advent_of_code.utils import read_input_stripped, solve, Coord, Vector, test


class Direction(Enum):
    N = Vector(0, -1)
    E = Vector(1, 0)
    S = Vector(0, 1)
    W = Vector(-1, 0)


DIR_FROM_CHAR = {"^": Direction.N, ">": Direction.E, "v": Direction.S, "<": Direction.W}


@dataclass
class Grid:
    robot: Coord
    boxes: set[Coord]
    walls: set[Coord]

    @property
    def size(self):
        return Coord(max(w.x for w in self.walls), max(w.y for w in self.walls))


def box_rh_half(box: Coord) -> Coord:
    """Rhs of box, given coord of lhs, for boxes 2 grid cells wide"""
    return Coord(box.x + 1, box.y)


def box_lh_half(box: Coord) -> Coord:
    """Lhs of box, given coord of rhs, for boxes 2 grid cells wide"""
    return Coord(box.x - 1, box.y)


@dataclass
class ParsedInputs:
    grid: Grid
    moves: list[Direction]


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_15.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day_15_sample.txt"))
    test(sample_inputs, part_1, "Part 1 test", expected=10092)
    solve(inputs, part_1, "Part 1")
    test(sample_inputs, part_2_with_render, "Part 2 test", expected=9021)
    solve(inputs, part_2_with_render, "Part 2")


def parse_inputs(inputs: list[str]) -> ParsedInputs:
    walls, boxes = set(), set()
    for y, line in enumerate(inputs):
        if not line:
            moves_start = y + 1
            break
        for x, char in enumerate(line):
            if char == "#":
                walls.add(Coord(x, y))
            if char == "O":
                boxes.add(Coord(x, y))
            if char == "@":
                robot = Coord(x, y)
    moves = [
        DIR_FROM_CHAR[char]
        for y, line in enumerate(inputs[moves_start:])
        for x, char in enumerate(line)
    ]
    return ParsedInputs(Grid(robot=robot, walls=walls, boxes=boxes), moves)


def move_robot(
    dir: Direction,
    grid: Grid,
    box_at_coord: Callable[[Coord, set[Coord]], bool],
    box_mover: Callable[[Coord, Direction, Grid], set[Coord] | None],
) -> Grid:
    attempt_robot_pos = grid.robot + dir.value
    if attempt_robot_pos in grid.walls:
        outcome = grid
    elif box_at_coord(attempt_robot_pos, grid.boxes):
        if (new_boxes := box_mover(attempt_robot_pos, dir, grid)) is None:
            outcome = grid
        else:
            outcome = Grid(robot=attempt_robot_pos, walls=grid.walls, boxes=new_boxes)
    else:
        outcome = Grid(robot=attempt_robot_pos, walls=grid.walls, boxes=grid.boxes)
    return outcome


def box_mover_pt1(start: Coord, dir: Direction, grid: Grid) -> set[Coord] | None:
    """Return boxes with positions updated in they can move one space in the direction dir,
    or None if move not possible"""
    assert start in grid.boxes, f"Start pos {start} must be a box"
    boxes_to_move = {start}
    next_pos = start
    while True:
        next_pos += dir.value
        if next_pos in grid.walls:
            return None
        elif next_pos in grid.boxes:
            boxes_to_move.add(next_pos)
        else:
            # Empty space - boxes can shunt along one
            moved_boxes = {b + dir.value for b in boxes_to_move}
            new_boxes = (grid.boxes - boxes_to_move).union(moved_boxes)
            assert len(new_boxes) == len(grid.boxes), "Different length boxes"
            return new_boxes


def transform_to_pt_2(pt_1: Grid) -> Grid:
    def double_x(c: Coord, plus: int = 0) -> Coord:
        return Coord(c.x * 2 + plus, c.y)

    walls = {double_x(w) for w in pt_1.walls}.union(double_x(w, plus=1) for w in pt_1.walls)
    boxes = {double_x(b) for b in pt_1.boxes}
    return Grid(robot=double_x(pt_1.robot), boxes=boxes, walls=walls)


def box_mover_pt2(start: Coord, dir: Direction, grid: Grid) -> set[Coord] | None:
    """For boxes that are two grid cells in width.
    Boxes tracked by recording the position of their LHS.
    Return boxes with positions updated in they can move one space in the direction dir,
    or None if move not possible."""
    if start in {box_rh_half(b) for b in grid.boxes}:
        # Robot trying to push RHS of box, which isn't tracked directly in grid.boxes
        start = box_lh_half(start)
    elif start not in grid.boxes:
        raise ValueError(f"Start pos {start} must be a box")
    boxes_not_yet_moved = copy.copy(grid.boxes)
    boxes_not_yet_moved.remove(start)
    moved_boxes_both_halves = {start + dir.value, box_rh_half(start) + dir.value}
    boxes_to_move = {start}
    while True:
        if any(m in grid.walls for m in moved_boxes_both_halves):
            return None
        more_boxes_to_move = {
            b
            for b in boxes_not_yet_moved
            if any(m in {b, box_rh_half(b)} for m in moved_boxes_both_halves)
        }
        if more_boxes_to_move:
            boxes_not_yet_moved -= more_boxes_to_move
            boxes_to_move |= more_boxes_to_move
            moved_boxes_both_halves |= {b + dir.value for b in more_boxes_to_move}
            moved_boxes_both_halves |= {box_rh_half(b) + dir.value for b in more_boxes_to_move}
        else:
            # Empty space - boxes can shunt along one
            moved_boxes = {b + dir.value for b in boxes_to_move}
            new_boxes = (grid.boxes - boxes_to_move).union(moved_boxes)
            assert len(new_boxes) == len(grid.boxes), "Different length boxes"
            return new_boxes


def box_at_coord_pt_1(comparable: Coord, boxes: set[Coord]) -> bool:
    return comparable in boxes


def box_at_coord_pt_2(comparable: Coord, boxes: set[Coord]) -> bool:
    return comparable in boxes.union(box_rh_half(b) for b in boxes)


def score(grid):
    return sum(100 * (c.y) + (c.x) for c in grid.boxes)


def part_1(inputs: ParsedInputs) -> int:
    grid = inputs.grid
    for i, move in enumerate(inputs.moves):
        grid = move_robot(move, grid, box_at_coord_pt_1, box_mover_pt1)
    return score(grid)


def part_2(inputs: ParsedInputs) -> int:
    grid = transform_to_pt_2(inputs.grid)
    for i, move in enumerate(inputs.moves):
        grid = move_robot(move, grid, box_at_coord_pt_2, box_mover_pt2)
    return score(grid)


def render_grid_pt_2(screen, grid: Grid) -> None:
    rhs_boxes = {box_rh_half(b) for b in grid.boxes}
    for y in range(grid.size.y + 1):
        for x in range(grid.size.x + 1):
            coord = Coord(x, y)
            if coord in grid.boxes:
                screen.addstr(y, x, "[", curses.color_pair(3))
            elif coord in rhs_boxes:
                screen.addstr(y, x, "]", curses.color_pair(3))
            elif coord in grid.walls:
                screen.addstr(y, x, "#", curses.color_pair(1))
            elif grid.robot == coord:
                screen.addstr(y, x, "@", curses.color_pair(2))
            else:
                screen.addstr(y, x, ".")


def part_2_with_render(inputs: ParsedInputs):
    def run(screen, grid: Grid):
        screen_y, screen_x = screen.getmaxyx()
        if grid.size.x > screen_x or grid.size.y > screen_y:
            raise ValueError(
                f"Terminal too small - zoom out. Got {(screen_x, screen_y)}, need: {grid.size}."
            )
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        screen.clear()
        for move in inputs.moves:
            render_grid_pt_2(screen, grid)
            screen.refresh()
            grid = move_robot(move, grid, box_at_coord_pt_2, box_mover_pt2)
            time.sleep(0.001)
        render_grid_pt_2(screen, grid)
        screen.refresh()
        return grid

    grid = curses.wrapper(run, transform_to_pt_2(inputs.grid))
    return score(grid)


if __name__ == "__main__":
    main()
