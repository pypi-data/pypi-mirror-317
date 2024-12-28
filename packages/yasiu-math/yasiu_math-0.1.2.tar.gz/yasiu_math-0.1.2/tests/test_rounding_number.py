import numpy as np
import pytest

from yasiu_math.math import round_number


num_list = np.linspace(0, 9.55553222, 150)

big_numb_list = np.linspace(100, 5555, 100)


@pytest.mark.parametrize("num", num_list)
def test_1_string_length_small(num):
    max_size = 5
    ret = round_number(num, max_size - 2)
    assert len(str(ret)) <= max_size


@pytest.mark.parametrize("num", num_list)
def test_2_value_small(num):
    max_size = 5
    ret = round_number(num, max_size)
    assert ret == np.round(num, max_size - 2)


@pytest.mark.parametrize("num", big_numb_list)
def test_2_value_big(num):
    max_size = 3
    ret = round_number(num, max_size)
    assert ret == np.round(num, 0)


@pytest.mark.parametrize("num", big_numb_list)
def test_3_big_num(num):
    max_size = 5
    ret = round_number(num, max_size)
    assert len(str(ret)) <= max_size


@pytest.mark.parametrize("num", big_numb_list)
def test_4_too_big_number(num):
    """Shrink too big number"""
    max_size = 3
    max_size += 1
    ret = round_number(num, max_size)
    assert len(str(
        ret)) <= max_size, f"Input: {num}, got: {ret} ({str(ret)}). Max size is: {max_size}, but got: {len(str(ret))}"
    # assert ret == np.round(num, 0)
