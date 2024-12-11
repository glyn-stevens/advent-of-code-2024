from pytest import fixture
from advent_of_code.day_11 import part_1, part_2, parse_inputs
from advent_of_code.utils import read_input_strippepoetry env use  C:\Users\Glyn\AppData\Local\Programs\Python\Python312-32\python.exed


@fixture
def inputs():
    return parse_inputs(read_input_stripped("day_11.txt"))


def test_part_1(inputs):
    assert part_1(inputs) == 233050

def test_part_2(inputs):
    assert part_2(inputs) == 276661131175807