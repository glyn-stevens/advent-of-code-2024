from pytest import fixture
from advent_of_code.day_4 import part_1, part_2
from advent_of_code.utils import read_input

@fixture
def input():
    return read_input(day=4)
    
def test_part_1(input):
    assert part_1(input) == 2571
    
def test_part_2(input):
    assert part_2(input) == 1992
