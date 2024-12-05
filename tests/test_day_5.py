from pytest import fixture
from advent_of_code.day_5 import part_1
from advent_of_code.utils import read_input


@fixture
def input():
    return read_input("day_5.txt")


def test_part_1(input):
    assert part_1(input) == 5268

