from pytest import fixture
from advent_of_code.day_22 import part_1, part_2, parse_inputs, n_secret_numbers
from advent_of_code.utils import read_input_stripped

def test_n_secret_numbers():
    sample_nums = [
        123,
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]
    assert n_secret_numbers(sample_nums[0], n=len(sample_nums)-1) == sample_nums

@fixture
def inputs():
    return parse_inputs(read_input_stripped("day_22.txt"))

def test_part_1(inputs):
    assert part_1(inputs) == 18525593556

def test_part_2(inputs):
    assert part_2(inputs) == 2089

