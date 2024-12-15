from pytest import fixture
from advent_of_code.day_14 import part_1, part_2, parse_inputs, Area, Robot
from advent_of_code.utils import read_input_stripped, Coord, Vector


@fixture
def inputs():
    return Area(parse_inputs(read_input_stripped("day_14.txt")), Coord(100, 102))


def test_part_1(inputs):
    assert part_1(inputs) == 231782040

def test_part_2(inputs):
    assert part_2(inputs) == 6475
