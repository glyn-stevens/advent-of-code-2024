import pytest
from pytest import fixture
from advent_of_code.day_16 import part_1, part_2, parse_inputs, coords_between
from advent_of_code.utils import read_input_stripped, Coord, Vector


@fixture
def inputs():
    return parse_inputs(read_input_stripped("day_16.txt"))

@pytest.mark.parametrize(("a", "b", "expected"),
    (
            [Coord(0,0), Coord(0,2), {Coord(0,0), Coord(0,1), Coord(0,2)}],
            [Coord(2,2), Coord(0,2), {Coord(0,2), Coord(1,2), Coord(2,2)}],
    )
                         )
def test_coords_between(a: Coord, b: Coord, expected: set[Coord]):
    assert coords_between(a, b) == expected
    assert coords_between(b, a) == expected


def test_part_1(inputs):
    assert part_1(inputs) == 99488

def test_part_2(inputs):
    assert part_2(inputs) == 516
