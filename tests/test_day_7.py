import itertools
from pickle import FALSE

from pytest import fixture, mark
from advent_of_code.day_7 import part_1, part_2_brute_force, parse_inputs, is_match_by_final_digits, part_2_fast, \
    combinations
from advent_of_code.utils import read_input
from more_itertools import distinct_permutations

@fixture
def inputs():
    return parse_inputs(read_input("day_7.txt"))


def test_part_1(inputs):
    assert part_1(inputs) == 2941973819040

@mark.parametrize(
    ("target", "test", "expected"),
     ([1234, 4, True], [1234, 1234, True], [123, 234, False], [143627, 7, True], [14362, 2, True])
)
def test_is_match_by_final_digits(target, test, expected):
    assert is_match_by_final_digits(target, test) == expected

def test_part_2(inputs):
    assert part_2_fast(inputs) == 249943041417600
