from pytest import fixture
from advent_of_code.day_4 import part_1, part_2
from advent_of_code.utils import read_input

@fixture
def inputs():
    return read_input("day_4.txt")
    
def test_part_1(inputs):
    assert part_1(inputs) == 2571
    
def test_part_2(inputs):
    assert part_2(inputs) == 1992
