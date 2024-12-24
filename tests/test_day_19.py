import pytest
from pytest import fixture
from advent_of_code.day_19 import part_1, part_2, parse_inputs
from advent_of_code.utils import read_input_stripped, Coord, Vector


@fixture
def inputs():
    return parse_inputs(read_input_stripped("day_19.txt"))

def test_part_1(inputs):
    assert part_1(inputs) == 369

def test_part_2(inputs):
    assert part_2(inputs) == 761826581538190
