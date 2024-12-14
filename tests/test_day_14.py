from pytest import fixture
from advent_of_code.day_14 import part_1, part_2, parse_inputs, Area
from advent_of_code.utils import read_input_stripped, Coord


@fixture
def inputs():
    return Area(parse_inputs(read_input_stripped("day_14.txt")), Coord(101, 103))


def test_part_1(inputs):
    assert part_1(inputs) == 231782040

# def test_part_2(inputs):
#     assert part_2(inputs) == 73267584326867
