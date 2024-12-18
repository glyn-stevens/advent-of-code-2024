from __future__ import annotations
import functools
import math
from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property
from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test, Coord, parse_args, configure_logging

import logging
import heapq


class Direction(Enum):
    N = auto()
    E = auto()
    S = auto()
    W = auto()

    def __repr__(self):
        return self.name


OPPOSITE_DIR = {
    Direction.N: Direction.S,
    Direction.S: Direction.N,
    Direction.E: Direction.W,
    Direction.W: Direction.E,
}


@dataclass(frozen=True)
class State:
    coord: Coord
    dir: Direction

    def __lt__(self, other: State):
        # Compare by coord first; if coords are equal, compare by direction
        if self.coord == other.coord:
            return self.dir.value < other.dir.value
        return self.coord < other.coord


@dataclass(frozen=True)
class Node:
    coord: Coord
    dirs_out: tuple[Direction, ...]

    @cached_property
    def dirs_in(self) -> set[Direction]:
        return {OPPOSITE_DIR[d] for d in self.dirs_out}


@dataclass(frozen=True)
class Grid:
    nodes: dict[Coord, Node]
    walls: set[Coord]
    start: Node
    end: Node


def main():
    args=parse_args()
    configure_logging(args)
    logging.info(f"Running script {Path(__file__).name}...")
    inputs = parse_inputs(read_input_stripped("day_16.txt"))
    sample_inputs = parse_inputs(read_input_stripped("day_16_sample.txt"))
    sample_inputs2 = parse_inputs(read_input_stripped("day_16_sample2.txt"))
    sample_inputs3 = parse_inputs(read_input_stripped("day_16_sample3.txt"))
    sample_inputs4 = parse_inputs(read_input_stripped("day_16_sample4.txt"))
    test(sample_inputs, part_1, "Part 1 test 1", expected=11048)
    test(sample_inputs2, part_1, "Part 1 test 2", expected=7036)
    test(sample_inputs3, part_1, "Part 1 test 3", expected=21148)
    test(sample_inputs4, part_1, "Part 1 test 4", expected=4013)
    input()
    solve(inputs, part_1, "Part 1")


PLAIN_PATH_CHAR = "."
END = "E"
START = "S"
WALL = "#"
ALL_PATH_CHARS = [PLAIN_PATH_CHAR, END, START]


def parse_inputs(inputs: list[str]) -> Grid:
    nodes = dict()
    walls = set()
    start, end = None, None
    for y, line in enumerate(inputs):
        for x, char in enumerate(line):
            if char in ALL_PATH_CHARS:
                node = parse_node(inputs, x, y)
                if node is not None:
                    nodes[node.coord] = node
                if char == START:
                    start = node
                elif char == END:
                    end = node
            elif char == WALL:
                walls.add(Coord(x, y))
            else:
                raise ValueError(f"Unexpected char in input: {char}")
    if not start or not end:
        raise ValueError(f"Grid not defined: {start=}, {end=}")
    return Grid(nodes, end=end, start=start, walls=walls)


def parse_node(inputs: list[str], x: int, y: int) -> Node | None:
    dirs_out = []
    if inputs[y - 1][x] in ALL_PATH_CHARS:
        dirs_out.append(Direction.N)
    if inputs[y + 1][x] in ALL_PATH_CHARS:
        dirs_out.append(Direction.S)
    if inputs[y][x + 1] in ALL_PATH_CHARS:
        dirs_out.append(Direction.E)
    if inputs[y][x - 1] in ALL_PATH_CHARS:
        dirs_out.append(Direction.W)
    if inputs[y][x] in {START, END}:
        # Always count the start and end as nodes
        return Node(Coord(x, y), tuple(dirs_out))
    if len(dirs_out) == 2 and dirs_out[0] == OPPOSITE_DIR[dirs_out[1]]:
        return None
    else:
        return Node(Coord(x, y), tuple(dirs_out))


def route_available(dir: Direction, current: Coord, to: Node) -> bool:
    match dir:
        case Direction.N:
            makeable = current.x == to.coord.x and current.y > to.coord.y
        case Direction.S:
            makeable = current.x == to.coord.x and current.y < to.coord.y
        case Direction.E:
            makeable = current.y == to.coord.y and current.x < to.coord.x
        case Direction.W:
            makeable = current.y == to.coord.y and current.x > to.coord.x
    return makeable


def distance(current: Coord, query: Coord) -> int:
    assert current.x == query.x or current.y == query.y
    return int(math.sqrt((current.x - query.x) ** 2 + (current.y - query.y) ** 2))


def next_node_in_dir(dir: Direction, current: Coord, all: set[Node]) -> Node | None:
    reachable_from_current = functools.partial(route_available, dir, current)
    potential_nodes = [n for n in all if reachable_from_current(n)]
    if potential_nodes:
        next_node = sorted(potential_nodes, key=lambda n: distance(current, n.coord))[0]
        if dir in next_node.dirs_in:
            return next_node
        else:
            # Wall in between nodes
            return None
    else:
        # No nodes at all in this direction
        return None


def part_1(grid: Grid) -> int:
    graph = build_graph_states(grid)
    score = dijkstra(grid, graph)
    return score


def build_graph_states(grid: Grid) -> dict[State, list[tuple[int, State]]]:
    """Build Graph, creating edges for:
    - Forward edges: from (node, direction) go straight until next node or blocked.
    - Turn edges: from (node, direction) to (node, direction)"""
    graph = {}
    for node in grid.nodes.values():
        for d in Direction:
            state = State(node.coord, d)
            edges = []
            # Possible turn edges:
            for d2 in node.dirs_out:
                if d2 != d:
                    cost = 2000 if d2 == OPPOSITE_DIR[d] else 1000
                    edges.append((cost, State(node.coord, d2)))
            # Possible forward edge:
            next_node = next_node_in_dir(d, node.coord, set(grid.nodes.values()))
            if next_node is not None:
                cost = distance(node.coord, next_node.coord)
                edges.append((cost, State(next_node.coord, d)))
            graph[state] = edges
    return graph


def dijkstra(grid: Grid, graph: dict[State, list[tuple[int, State]]]):
    start_state = State(grid.start.coord, Direction.E)  # Starting state as defined in puzzle

    cost_map: dict[State, float] = {}
    for node_coord in grid.nodes:
        for d in Direction:
            cost_map[State(node_coord, d)] = math.inf
    cost_map[start_state] = 0

    priority_queue = []
    heapq.heappush(priority_queue, (cost_map[start_state], start_state))

    while priority_queue:
        current_cost, state = heapq.heappop(priority_queue)
        if current_cost > cost_map[state]:
            continue
        if state.coord == grid.end.coord:
            return current_cost
        for cost_to_adjacent, adjacent_state in graph[state]:
            candidate_cost = current_cost + cost_to_adjacent
            if candidate_cost < cost_map[adjacent_state]:
                cost_map[adjacent_state] = candidate_cost
                heapq.heappush(priority_queue, (candidate_cost, adjacent_state))
    return None

def display(path_: list[Node], walls: set[Coord]) -> None:
    for y in range(max(n.coord.y+2 for n in path_)):
        line = ""
        for x in range(max(n.coord.x+2 for n in path_)):
            coord = Coord(x, y)
            path_idx = next((i for i, path_pt in enumerate(path_) if path_pt.coord == coord), None)
            if coord in walls:
                line += "#"
                if path_idx is not None:
                    raise ValueError
            elif path_idx is not None:
                line += str(path_idx)[-1]
            else:
                line += "."
        print(line)

if __name__ == "__main__":
    main()
