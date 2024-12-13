from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test, Coord


class Direction(Enum):
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)


@dataclass(frozen=True)
class Edge:
    """An Edge at cell=(x,y), side=Direction.N means the cell at (x,y) has an edge/border on it's top side"""

    cell: Coord
    side: Direction

    def __repr__(self):
        return f"[{self.cell}, {self.side.name}]"


@dataclass(frozen=True)
class Region:
    cells: set[Coord]
    edges: set[Edge]


def move(coord: Coord, dir: Direction) -> Coord:
    return Coord(coord.x + dir.value[0], coord.y + dir.value[1])


def perpendicular_dirs(dir: Direction) -> tuple[Direction, Direction]:
    if dir in [Direction.N, Direction.S]:
        return (Direction.E, Direction.W)
    else:
        return (Direction.N, Direction.S)


def get_value_at(coord: Coord, map_: list[str]) -> str:
    return map_[coord.y][coord.x]


def in_grid(coord: Coord, map_: list[str]) -> bool:
    return 0 <= coord.x < len(map_[0]) and 0 <= coord.y < len(map_)


def is_adjacent(a: Edge, b: Edge) -> bool:
    return a.side == b.side and b.cell in [move(a.cell, p) for p in perpendicular_dirs(a.side)]


def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = read_input_stripped("day_12.txt")
    sample_inputs = read_input_stripped("day_12_sample.txt")
    test(sample_inputs, part_1, "Part 1 test", expected=1930)
    solve(inputs, part_1, "Part 1")
    test(sample_inputs, part_2, "Part 2 test", expected=1206)
    solve(inputs, part_2, "Part 2")


def extract_regions(grid: list[str]) -> list[Region]:
    regions: list[Region] = []
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            plot = Coord(x, y)
            if any(plot in region.cells for region in regions):
                # Plot has already been assigned to a region
                continue
            else:
                plots, edges = find_cells_edges_in_region(plot, set(), grid)
                regions.append(Region(cells=plots, edges=edges))
    return regions


def find_cells_edges_in_region(
    investigating: Coord, cells_in_region: set[Coord], grid: list[str]
) -> tuple[set[Coord], set[Edge]]:
    region_value = get_value_at(investigating, grid)
    edges: set[Edge] = set()
    cells_in_region.add(investigating)
    for dir in Direction:
        adjacent_cell = move(investigating, dir)
        if adjacent_cell in cells_in_region:
            # Already visited this cell, and no edge of region here
            continue
        elif not in_grid(adjacent_cell, grid) or get_value_at(adjacent_cell, grid) != region_value:
            # Moved over the boundary of the region -> edge found
            edges.add(Edge(investigating, dir))
        else:
            # Adjacent cell is in region. Recursively find cells and edges from that cell.
            plots_to_add, edges_to_add = find_cells_edges_in_region(
                adjacent_cell, cells_in_region, grid
            )
            cells_in_region |= plots_to_add
            edges |= edges_to_add
    return cells_in_region, edges


def extract_sides(bag_of_edges: set[Edge]) -> list[set[Edge]]:
    sides: list[set[Edge]] = []
    # Sort edges so that each edge in a side are looped through in order
    for edge in sorted(bag_of_edges, key=lambda e: (e.cell.x, e.cell.y)):
        for side in sides:
            if any(is_adjacent(edge, edge_in_side) for edge_in_side in side):
                side.add(edge)
                continue
        if edge not in [e for edges in sides for e in edges]:
            sides.append({edge})
    return sides


def part_1(inputs: list[str]) -> int:
    regions = extract_regions(inputs)
    return sum(len(region.edges) * len(region.cells) for region in regions)


def part_2(inputs: list[str]) -> int:
    regions = extract_regions(inputs)
    return sum(len(extract_sides(region.edges)) * len(region.cells) for region in regions)


if __name__ == "__main__":
    main()
