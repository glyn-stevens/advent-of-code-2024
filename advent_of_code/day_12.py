from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from advent_of_code.utils import read_input_stripped, solve, test, Coord


@dataclass(frozen=True)
class Region:
    plots: set[Coord]
    perimeter: int

class Direction(Enum):
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)

def move(coord: Coord, dir: Direction) -> Coord:
    return Coord(coord.x + dir.value[0], coord.y + dir.value[1])

def get_value_at(coord: Coord, map_: list[str]) -> str:
    return map_[coord.y][coord.x]

def in_grid(coord: Coord, map_: list[str]) -> bool:
    return 0 <= coord.x < len(map_[0]) and 0 <= coord.y < len(map_)

def main():
    print(f"Running script {Path(__file__).name}...")
    inputs = read_input_stripped("day_12.txt")
    sample_inputs = read_input_stripped("day_12_sample.txt")
    test(sample_inputs, part_1, "Part 1 test", expected=1930)
    solve(inputs, part_1, "Part 1")
    test(sample_inputs, part_2, "Part 2 test", expected=1206)
    solve(inputs, part_2, "Part 2")

def extract_regions(map_: list[str]) -> list[Region]:
    regions: list[Region] = []
    for y, line in enumerate(map_):
        for x, char in enumerate(line):
            plot = Coord(x,y)
            if any(plot in region.plots for region in regions):
                # Plot has already been assigned to a region
                continue
            else:
                plots, perimeter = all_plots_in_region(plot, map_, set())
                regions.append(Region(plots=plots, perimeter=perimeter))
    return regions

def all_plots_in_region(plot_to_include: Coord, map_: list[str], plots_included: set[Coord]) -> tuple[set[Coord], int]:
    region_value = get_value_at(plot_to_include, map_)
    # print(f"For region {region_value}: Checking {plot_to_include=}, {plots_included=}")
    perimiter = 0
    plots_included.add(plot_to_include)
    for dir in Direction:
        potential_plot_to_include = move(plot_to_include, dir)
        if potential_plot_to_include in plots_included:
            continue
        elif not in_grid(potential_plot_to_include, map_) or get_value_at(potential_plot_to_include, map_) != region_value:
            perimiter += 1
        else:
            plots_to_add, perim_to_add = all_plots_in_region(potential_plot_to_include, map_, plots_included)
            plots_included |= plots_to_add
            perimiter += perim_to_add

    return plots_included, perimiter



def part_1(inputs: list[str]) -> int:
    regions = extract_regions(inputs)
    return sum(region.perimeter*len(region.plots) for region in regions)

def part_2(inputs: list[str]) -> int:
    return 0

if __name__ == "__main__":
    main()
