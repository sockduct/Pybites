'''
In this Bite you test a simple number guessing game (class). Ready to write some
pytest code? Read on ...

You again will need to mock out a standard library function, input this time.

We tried to use random.randint to get the secret number, but mutation testing
became a bit too strict on us, so for now we just pass the secret number into
the constructor. That said, there is some validation going on that you will need
to test. Check for boundaries and to check exception strings, pytest's raises
has a nice match kwarg.

The constructor also takes an optional max_guesses arg to make the game easier
or harder. You will need to the use capfd/capsys fixture again to test the
standard output of the game (100% test coverage remember).

Good luck and keep calm and code in Python / pytest.
'''

from pathlib import Path
import sys
from unittest.mock import patch

# Allow importing from local directory for pytest:
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest

from guess import GuessGame, InvalidNumber


# write test code to reach coverage + make mutatest happy
@pytest.fixture()
def game() -> GuessGame:
    return GuessGame(8, max_guesses=4)


@pytest.mark.parametrize('number, result', [
    ('not_a_number', 'Not a number'),
    (-100, 'Negative number'),
    (-1, 'Negative number'),
    (0, int()),
    (7, int()),
    (14, int()),
    (15, int()),
    (16, 'Number too high'),
    (100, 'Number too high')
])
def test_validate(number: int, result: InvalidNumber|int, game: GuessGame) -> None:
    if isinstance(result, str):
        with pytest.raises(InvalidNumber) as exc:
            game._validate(number)
            assert str(exc.value) == result
    else:
        assert game._validate(number) == number
