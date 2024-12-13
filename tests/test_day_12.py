from pytest import fixture
from advent_of_code.day_12 import part_1, part_2
from advent_of_code.utils import read_input_stripped


@fixture
def inputs():
    return read_input_stripped("day_12.txt")


def test_part_1(inputs):
    assert part_1(inputs) == 1467094

def test_part_2(inputs):
    assert part_2(inputs) == 881182
