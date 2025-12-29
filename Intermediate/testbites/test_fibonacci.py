#! /usr/bin/env python3.14
'''
We moved from mutpy (<= 3.7) to mutatest (3.12 📈) for test Bites.

First we check if you have 90% test coverage, then we inject some mutations into
the code to see if your tests catch them. 🤯

Good luck 🔥 💪 (please be patient 🙏 - it can take a few seconds to run the
tests 🕒)

Our first Test Bite! The concept is simple: to pass a Test Bite, you write tests
for the program under the "Code to Test" tab.

We run pytest-cov and mutatest against your code to see if your tests are strong
enough.

To kick this off we have you write some tests for fib which generates a
Fibonacci sequence.

Note that we use the functool.cache decorator so we can also test higher numbers
without timing out.
'''

import sys

sys.path.append('.')

import pytest

from fibonacci import fib

# write one or more pytest functions below, they need to start with test_
#
# Test Plan:
# * negative number => ValueError
# * 0 => 0
# * 1 => 1
# * 2 => 1
# * 3 => 2
# * 4 => 3
# * 5 => 5
# * 10 => 55
# * 25 => 75025

def test_negative() -> None:
    with pytest.raises(ValueError):
        fib(-1)

@pytest.mark.parametrize('n, expected', [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (10, 55),
    (25, 75025)
])
def test_vals(n, expected) -> None:
    assert fib(n) == expected
