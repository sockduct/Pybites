#! /usr/bin/env python3.14


'''
Our 4th test Bite. Michael made a calculator that will be able to accept a list
of decimal digits and returns an integer where each int of the given list
represents decimal place values from first element to last.

He wrote the function in such a way that it only accepts positive digits in
range(0, 10) and anything that is not raises a ValueError if its out of range,
or a TypeError if its not an int type.

Some examples:
[0, 4, 2, 8] => 428
[1, 2] => 12
[3] => 3
[6, 2, True] => raises TypeError
[-3, 12] => raises ValueError
[3.6, 4, 1] => raises TypeError
['4', 5, 3, 1] => raises TypeError

In this Bite you are tasked to write the tests for this function. Good luck and
keep calm and code in Python!
'''

import sys

# Need to insert at beginning versus appending to end for pytest-cov to work
# correctly - alternatively could define $PYTHONPATH=`CWD`:
sys.path.insert(0, '.')

import pytest

from numbers_to_dec import list_to_decimal


def test_type1() -> None:
    with pytest.raises(TypeError):
        list_to_decimal(['a', 'b', 'c'])  # type: ignore


def test_type2() -> None:
    with pytest.raises(TypeError):
        list_to_decimal([True, False])


def test_type3() -> None:
    with pytest.raises(TypeError):
        list_to_decimal([5.7, 9.2])  # type: ignore


def test_type4() -> None:
    with pytest.raises(TypeError):
        list_to_decimal([1, 5, 7.9])  # type: ignore


def test_nums1() -> None:
    with pytest.raises(ValueError):
        list_to_decimal([1, -5])


def test_nums2() -> None:
    with pytest.raises(ValueError):
        list_to_decimal([1, 0, 3, -1])


def test_nums3() -> None:
    with pytest.raises(ValueError):
        list_to_decimal([1, 3, 10])


@pytest.mark.parametrize('values, expected', [
    ([0, 4, 2, 8], 428),
    ([1, 2], 12),
    ([3], 3),
    ([7, 3, 5, 0], 7350)
])
def test_nums4(values: list[int], expected: int) -> None:
    assert list_to_decimal(values) == expected


'''
Solution - better test names:
@pytest.mark.parametrize(
    "arg, expected", [([0, 4, 2, 8], 428), ([1, 2], 12), ([3, 5, 1], 351)]
)
def test_valid_input(arg, expected):
    assert list_to_decimal(arg) == expected


def test_value_error_lt_min():
    with pytest.raises(ValueError):
        list_to_decimal([-3, 2, 1])


def test_value_error_gt_max():
    with pytest.raises(ValueError):
        list_to_decimal([2, 1, 10])


def test_type_error_str():
    with pytest.raises(TypeError):
        list_to_decimal(["str", 2, 1])


def test_type_error_float():
    with pytest.raises(TypeError):
        list_to_decimal([1, 2, 3.6])
'''
