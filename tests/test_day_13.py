from pytest import fixture
from advent_of_code.day_13 import part_1, part_2, parse_inputs
from advent_of_code.utils import read_input_stripped


@fixture
def inputs():
    return parse_inputs(read_input_stripped("day_13.txt"))


def test_part_1(inputs):
    assert part_1(inputs) == 39996

def test_part_2(inputs):
    assert part_2(inputs) == 73267584326867
