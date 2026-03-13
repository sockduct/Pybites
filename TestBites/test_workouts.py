#! /usr/bin/env python


'''
In this Bite you test a function that prints to stdout. Check out pytest's
Capturing of the stdout/stderr output how to test this.

You probably want to use the capsys / capfd fixture in your test code and you'll
probably find a good use case for @pytest.mark.parametrize here too.

Have fun and keep calm and code in Python!
'''


import pytest

from workouts import print_workout_days


'''
Tests:
* Non-string (e.g., None, 5) => AttributeError
* '' => Mon, ..., Fri (all)
* 'upper' => Mon, Thu
* 'cardio' => Wed
* '-' => No matching workout
'''
@pytest.mark.parametrize('value', [None, 5])
def test_bad_val(value: None|int) -> None:
    with pytest.raises(AttributeError):
        print_workout_days(value)  # type: ignore

@pytest.mark.parametrize('value, expected', [
    ('', 'Mon, Tue, Wed, Thu, Fri'),
    ('upper', 'Mon, Thu'),
    ('cardio', 'Wed'),
    ('-', 'No matching workout')
])
def test_vals(value: str, expected: str, capsys: pytest.CaptureFixture[str]) -> None:
    print_workout_days(value)
    captured = capsys.readouterr()
    assert captured.out.rstrip() == expected


'''
# Solution:
@pytest.mark.parametrize("arg, expected", [
    ('upper', 'Mon, Thu'),
    ('lower', 'Tue, Fri'),
    ('30', 'Wed'),
    ('30 min', 'Wed'),
    ('30 min cardio', 'Wed'),
    ('30 MIN CARDIO', 'Wed'),
    ('upper body #1', 'Mon'),
    ('upper body #2', 'Thu'),
    ('lower body #1', 'Tue'),
    ('lower body #2', 'Fri'),
    ('Upper', 'Mon, Thu'),
    ('UPPEr', 'Mon, Thu'),
    ('Upper Body #', 'Mon, Thu'),
    ('lower upper body', 'No matching workout'),
    ('sun', 'No matching workout'),
    ('30 min cardio -', 'No matching workout'),
    ('nonsense', 'No matching workout'),
])
def test_print_workout_days(arg, expected, capfd):
    print_workout_days(arg)
    actual = capfd.readouterr()[0].strip()
    assert actual == expected
'''
