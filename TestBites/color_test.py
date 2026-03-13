#! /usr/bin/env python


'''
We moved from mutpy (<= 3.7) to mutatest (3.12 📈) for test Bites.

First we check if you have 90% test coverage, then we inject some mutations into
the code to see if your tests catch them. 🤯

Good luck 🔥 💪 (please be patient 🙏 - it can take a few seconds to run the
tests 🕒)

In this Bite you will mock out a function of the standard library, more
specifically random.sample.

We wrote a small generator that produces hex colors. We also provided a fixture
to initialize the generator so you can just call next(gen) to get the next hex
value.

Use unittest.mock's patch to mock out the call to sample. It might be a bit
tricky, but once you get this one down you possess a valuable testing skill!

Have fun and keep calm and test with pytest!
'''


from collections.abc import Generator, Iterator
import re
from unittest.mock import MagicMock, patch

import pytest


from . import color


@pytest.fixture(scope="module")
def gen() -> Generator[Iterator[str], None, None]:
    # Note:  patch('color.sample', sample_mock) doesn't work - can't find color
    with patch.object(color, 'sample', MagicMock(return_value=[128, 128, 128])):
        # Note:  return color.gen_hex_color() doesn't work - patch fails...
        yield color.gen_hex_color()

def test_gen_hex_color_str(gen: Iterator[str]) -> None:
    res = next(gen)
    assert isinstance(res, str)
    assert res.startswith('#')

def test_gen_hex_color_len(gen: Iterator[str]) -> None:
    res = next(gen)
    assert len(res) == 7

def test_gen_hex_color_pattern(gen: Iterator[str]) -> None:
    res = next(gen)
    assert re.match(r'#[0-9A-F]{6}', res)

def test_gen_hex_mock(gen: Iterator[str]) -> None:
    res = next(gen)
    assert res == '#808080'


'''
# Provided solution:
@patch.object(color, "sample", side_effect=[
    [191, 165, 216],
    [101, 102, 103]
])
def test_gen_hex_color(mock, gen):
    assert next(gen) == "#BFA5D8"
    assert next(gen) == "#656667"
'''