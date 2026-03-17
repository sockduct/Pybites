from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest


spec = spec_from_file_location("guess", Path(__file__).with_name("guess.py"))
guess = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(guess)

GuessGame = guess.GuessGame
InvalidNumber = guess.InvalidNumber
MAX_NUMBER = guess.MAX_NUMBER


def test_init_sets_secret_number_max_guesses_and_attempt():
    game = GuessGame(7, max_guesses=3)

    assert game.secret_number == 7
    assert game.max_guesses == 3
    assert game.attempt == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("0", 0),
        (0, 0),
        (MAX_NUMBER, MAX_NUMBER),
        ("15", MAX_NUMBER),
    ],
)
def test_validate_accepts_ints_and_numeric_strings_within_range(value, expected):
    game = GuessGame(1)

    assert game._validate(value) == expected


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ("not-a-number", "Not a number"),
        (-1, "Negative number"),
        ("-3", "Negative number"),
        (MAX_NUMBER + 1, "Number too high"),
        (str(MAX_NUMBER + 1), "Number too high"),
    ],
)
def test_validate_rejects_invalid_values(value, message):
    game = GuessGame(1)

    with pytest.raises(InvalidNumber, match=message):
        game._validate(value)


@pytest.mark.parametrize(
    ("secret_number", "message"),
    [
        ("bad", "Not a number"),
        (-1, "Negative number"),
        (MAX_NUMBER + 1, "Number too high"),
    ],
)
def test_init_validates_secret_number(secret_number, message):
    with pytest.raises(InvalidNumber, match=message):
        GuessGame(secret_number)


def test_call_prints_too_low_then_success_and_stops(monkeypatch, capsys):
    guesses = iter(["2", "5", "9"])
    game = GuessGame(5, max_guesses=4)

    monkeypatch.setattr("builtins.input", lambda: next(guesses))

    game()

    captured = capsys.readouterr()
    assert captured.out == (
        "Guess a number: \n"
        "Too low\n"
        "Guess a number: \n"
        "You guessed it!\n"
    )
    assert game.attempt == 2


def test_call_prints_too_high(monkeypatch, capsys):
    game = GuessGame(3, max_guesses=1)
    monkeypatch.setattr("builtins.input", lambda: "8")

    game()

    captured = capsys.readouterr()
    assert captured.out == (
        "Guess a number: \n"
        "Too high\n"
        "Sorry, the number was 3\n"
    )
    assert game.attempt == 1


def test_call_reprompts_after_non_numeric_input_without_using_attempt(monkeypatch, capsys):
    guesses = iter(["hello", "4"])
    game = GuessGame(4, max_guesses=1)

    monkeypatch.setattr("builtins.input", lambda: next(guesses))

    game()

    captured = capsys.readouterr()
    assert captured.out == (
        "Guess a number: \n"
        "Enter a number, try again\n"
        "Guess a number: \n"
        "You guessed it!\n"
    )
    assert game.attempt == 1


def test_call_prints_sorry_after_exhausting_all_guesses(monkeypatch, capsys):
    guesses = iter(["1", "2", "3"])
    game = GuessGame(4, max_guesses=3)

    monkeypatch.setattr("builtins.input", lambda: next(guesses))

    game()

    captured = capsys.readouterr()
    assert captured.out == (
        "Guess a number: \n"
        "Too low\n"
        "Guess a number: \n"
        "Too low\n"
        "Guess a number: \n"
        "Too low\n"
        "Sorry, the number was 4\n"
    )
    assert game.attempt == 3


def test_call_with_zero_allowed_guesses_immediately_reveals_answer(capsys):
    game = GuessGame(6, max_guesses=0)

    game()

    captured = capsys.readouterr()
    assert captured.out == "Sorry, the number was 6\n"
    assert game.attempt == 0
