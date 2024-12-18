from pytest import fixture
from advent_of_code.day_15 import part_1, part_2, parse_inputs
from advent_of_code.day_16 import PathPoint, Direction, switch_route_to
from advent_of_code.utils import read_input_stripped, Coord, Vector


@fixture
def inputs():
    return parse_inputs(read_input_stripped("day_15.txt"))

def test_switch_route():
    originals = [[PathPoint(Coord(0,0), Direction.N),PathPoint(Coord(1,1), Direction.N),PathPoint(Coord(2,2), Direction.N), PathPoint(Coord(4,4), Direction.N), PathPoint(Coord(5,5), Direction.N)]]
    replacement = [PathPoint(Coord(0,0), Direction.N), PathPoint(Coord(4,4), Direction.N)]
    coord =  PathPoint(Coord(4,4), Direction.N)
    switch_route_to(coord, originals, replacement)

    assert originals == [PathPoint(Coord(0,0), Direction.N), PathPoint(Coord(4,4), Direction.N), PathPoint(Coord(5,5), Direction.N)]

# def test_part_1(inputs):
#     assert part_1(inputs) == 1475249
#
# def test_part_2(inputs):
#     assert part_2(inputs) == 1509724
