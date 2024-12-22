import pytest
from pytest import fixture
from advent_of_code.day_17 import part_1, part_2, binary_append_3_bits, Machine
from advent_of_code.utils import read_input_stripped, Coord, Vector

@pytest.fixture(scope="function")
def inputs() -> Machine:
    return Machine(register_values=(46337277, 0, 0), program=[2,4,1,1,7,5,4,4,1,4,0,3,5,5,3,0])

@pytest.mark.parametrize(("value", "suffix", "expected"),
    (
            [int("100", base=2), int("100", base=2), int("100100", base=2)],
            [int("100", base=2), int("000", base=2), int("100000", base=2)],
            [int("111", base=2), int("000", base=2), int("111000", base=2)],
    )
                         )
def test_binary_append(value: int, suffix: int, expected: int):
    output = binary_append_3_bits(value, suffix)
    assert output == expected, f"Got {bin(output)}, expected  {bin(expected)}"


def test_part_1(inputs):
    assert part_1(inputs) == "7,4,2,0,5,0,5,3,7"

def test_part_2(inputs):
    assert part_2(inputs) == 202991746427434
