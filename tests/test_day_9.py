from pytest import fixture
from advent_of_code.day_9 import part_1, part_2, parse_inputs
from advent_of_code.utils import read_input_stripped


@fixture
def inputs():
    return parse_inputs(read_input_stripped("day_9.txt"))


def test_part_1(inputs):
    assert part_1(inputs) == 6370402949053

# def test_part_2(inputs):
#     assert part_2(inputs) ==
