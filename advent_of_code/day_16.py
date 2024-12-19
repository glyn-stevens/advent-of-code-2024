from __future__ import annotations

import copy
import functools
import math
from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property, lru_cache
from pathlib import Path
from typing import FrozenSet

from advent_of_code.utils import (
    read_input_stripped,
    solve,
    test,
    Coord,
    parse_args,
    configure_logging,
)

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
    nodes: FrozenSet[Node]
    walls: FrozenSet[Coord]
    start: Node
    end: Node


@dataclass(frozen=True)
class DijkstrasResults:
    min_cost: int | None
    path_graph: FrozenSet[tuple[State, FrozenSet[State]]]
    """Graph of cheapest previous States to visit from each State explored in to"""
    end_states: FrozenSet[State]
    """Cheapest set of end States (Coord and Direction) to reach"""


def main():
    args = parse_args()
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
    test(sample_inputs, part_2, "Part 2 test", expected=64)
    solve(inputs, part_1, "Part 1")
    solve(inputs, part_2, "Part 2")


PLAIN_PATH_CHAR = "."
END = "E"
START = "S"
WALL = "#"
ALL_PATH_CHARS = [PLAIN_PATH_CHAR, END, START]


def parse_inputs(inputs: list[str]) -> Grid:
    nodes = set()
    walls = set()
    start, end = None, None
    for y, line in enumerate(inputs):
        for x, char in enumerate(line):
            if char in ALL_PATH_CHARS:
                node = parse_node(inputs, x, y)
                if node is not None:
                    nodes.add(node)
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
    return Grid(frozenset(nodes), end=end, start=start, walls=frozenset(walls))


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


def coords_between(a: Coord, b: Coord) -> set[Coord]:
    if a.x == b.x:
        return {Coord(a.x, y) for y in range(min(a.y, b.y), max(a.y, b.y) + 1)}
    elif a.y == b.y:
        return {Coord(x, a.y) for x in range(min(a.x, b.x), max(a.x, b.x) + 1)}
    else:
        raise ValueError(
            "To calculate coords between two coords, they need to be in the same line"
        )


def next_node_in_dir(dir: Direction, current: Coord, all: FrozenSet[Node]) -> Node | None:
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
    result = dijkstra_search(grid, graph)
    path_graph = {state: states for state, states in result.path_graph}
    display(reconstruct_paths(path_graph, set(result.end_states)), grid.walls)
    if result.min_cost is None:
        raise ValueError("Score not calculated")
    return result.min_cost


def part_2(grid: Grid) -> int:
    graph = build_graph_states(grid)
    result = dijkstra_search(grid, graph)
    path_graph = {state: states for state, states in result.path_graph}
    coords_in_path = reconstruct_paths(path_graph, set(result.end_states))
    display(coords_in_path, grid.walls)
    if result.min_cost is None:
        raise ValueError("Score not calculated")
    return len(coords_in_path)


ImmutableCostGraph = FrozenSet[tuple[State, tuple[tuple[int, State], ...]]]


@lru_cache
def build_graph_states(grid: Grid) -> ImmutableCostGraph:
    """Build Graph, creating edges for:
    - Forward edges: from (node, direction) go straight until next node or blocked.
    - Turn edges: from (node, direction) to (node, direction)"""
    cost_graph = {}
    for node in grid.nodes:
        for d in Direction:
            state = State(node.coord, d)
            edges = []
            # Possible turn edges:
            for d2 in node.dirs_out:
                if d2 != d:
                    cost = 2000 if d2 == OPPOSITE_DIR[d] else 1000
                    edges.append((cost, State(node.coord, d2)))
            # Possible forward edge:
            next_node = next_node_in_dir(d, node.coord, grid.nodes)
            if next_node is not None:
                cost = distance(node.coord, next_node.coord)
                edges.append((cost, State(next_node.coord, d)))
            cost_graph[state] = edges
    return frozenset((state, tuple(edges)) for state, edges in cost_graph.items())


@lru_cache
def dijkstra_search(grid: Grid, cost_graph_immutable: ImmutableCostGraph) -> DijkstrasResults:
    logging.info("Starting search for cheapest path using Dijkstra's algorithm")
    start_state = State(grid.start.coord, Direction.E)  # Starting state as defined in puzzle
    cost_graph = {state: edges for state, edges in cost_graph_immutable}
    unexplored_end_states = {s for s in cost_graph.keys() if s.coord == grid.end.coord}
    all_end_states = copy.deepcopy(unexplored_end_states)
    logging.info(f"End states to explore to: {unexplored_end_states}")

    path_graph: dict[State, set[State]] = {}
    cost_map: dict[State, float] = {}
    for node in grid.nodes:
        for d in Direction:
            cost_map[State(node.coord, d)] = math.inf
    cost_map[start_state] = 0

    priority_queue: list[tuple[dict[State, float], State]] = []
    heapq.heappush(priority_queue, (cost_map[start_state], start_state))  # type: ignore

    while priority_queue:
        current_cost, state = heapq.heappop(priority_queue)
        if current_cost > cost_map[state]:  # type: ignore
            continue
        if state in unexplored_end_states:
            unexplored_end_states.remove(state)
            logging.debug(f"Explored state at end: {state}. {unexplored_end_states = }.")
            if len(unexplored_end_states) == 0:
                break
        for cost_to_adjacent, adjacent_state in cost_graph[state]:
            candidate_cost = current_cost + cost_to_adjacent  # type: ignore
            if candidate_cost <= cost_map[adjacent_state]:
                if candidate_cost < cost_map[adjacent_state]:
                    cost_map[adjacent_state] = candidate_cost
                    path_graph[adjacent_state] = {state}
                else:
                    path_graph.setdefault(adjacent_state, set())
                    path_graph[adjacent_state].add(state)
                heapq.heappush(priority_queue, (candidate_cost, adjacent_state))  # type: ignore
    explored_end_states = all_end_states - unexplored_end_states
    immutable_path_graph = frozenset((s, frozenset(prev_s)) for s, prev_s in path_graph.items())
    if explored_end_states:
        logging.info(f"Explored end states: {explored_end_states}")
        min_cost = min(cost_map[s] for s in explored_end_states)
        cheapest_end_stats = {e for e in explored_end_states if cost_map[e] == min_cost}
        return DijkstrasResults(int(min_cost), immutable_path_graph, frozenset(cheapest_end_stats))
    logging.error("Dijkstra's algo didn't find any end states")
    return DijkstrasResults(None, immutable_path_graph, frozenset())


def reconstruct_paths(
    path_map: dict[State, FrozenSet[State]], end_states: set[State]
) -> set[Coord]:
    coords_on_path = set()
    queue = end_states
    while queue:
        current_state = queue.pop()
        coords_on_path.add(current_state.coord)
        if current_state not in path_map:
            logging.info(f"State {current_state} in path but not in map - at start coord")
            continue
        for next_state in path_map[current_state]:
            coords_on_path.update(coords_between(current_state.coord, next_state.coord))
        queue.update(path_map[current_state])
    return coords_on_path


def display(paths: set[Coord], walls: FrozenSet[Coord]) -> None:
    for y in range(max(n.y + 1 for n in walls)):
        line = ""
        for x in range(max(n.x + 1 for n in walls)):
            coord = Coord(x, y)
            if coord in walls:
                line += "#"
            elif coord in paths:
                line += "0"
            else:
                line += "."
        print(line)


if __name__ == "__main__":
    main()
