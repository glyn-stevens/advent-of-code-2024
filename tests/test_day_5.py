from pytest import fixture
from advent_of_code.day_5 import part_1, part_2
from advent_of_code.utils import read_input


@fixture
def inputs():
    return read_input("day_5.txt")


def test_part_1(inputs):
    assert part_1(inputs) == 5268

def test_part_2(inputs):
    assert part_2(inputs) == 5799

