from pytest import fixture
from advent_of_code.day_6 import part_1, part_2
from advent_of_code.utils import read_input


@fixture
def input():
    return read_input("day_6.txt")


def test_part_1(input):
    assert part_1(input) == 5453

# def test_part_2(input):
#     assert part_2(input) == 5799

