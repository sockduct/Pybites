#! /usr/bin/env python
'''
We moved from mutpy (<= 3.7) to mutatest (3.12 📈) for test Bites.

First we check if you have 90% test coverage, then we inject some mutations into
the code to see if your tests catch them. 🤯

Good luck 🔥 💪 (please be patient 🙏 - it can take a few seconds to run the
tests 🕒)

In our second Test Bite you will write tests for FizzBuzz. Refer to the "Code to
Test" tab, then start to write your pytests. Have fun!
'''


import pytest

from .fizzbuzz import fizzbuzz


# write one or more pytest functions below, they need to start with test_
@pytest.mark.parametrize('num, expected', [
    (-4, -4),
    (-3, 'Fizz'),
    (-2, -2),
    (-1, -1),
    (0, 'Fizz Buzz'),
    (1, 1),
    (2, 2),
    (3, 'Fizz'),
    (4, 4),
    (5, 'Buzz'),
    (6, 'Fizz'),
    (7, 7),
    (8, 8),
    (9, 'Fizz'),
    (10, 'Buzz'),
    (15, 'Fizz Buzz')
])
def test_values(num: int, expected: int|str) -> None:
    actual = fizzbuzz(num)
    assert actual == expected
