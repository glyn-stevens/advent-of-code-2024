import pytest
from pytest import fixture
from advent_of_code.day_24 import part_1, parse_inputs, number_trailing_digits_correct
from advent_of_code.utils import read_input_stripped


@pytest.mark.parametrize(("a", "b", "expected"),
                         (
                                 ["1100", "1100", 4],
                                 ["1100", "1101", 0],
                                 ["1110", "1100", 1],
                                 ["01110", "1100", 1],
                         ))
def test_digits_correct(a:str, b:str, expected:float):
    assert number_trailing_digits_correct(a, b) == expected
@fixture
def inputs():
    return parse_inputs(read_input_stripped("day_24.txt"))

def test_part_1(inputs):
    assert part_1(inputs) == 49520947122770

