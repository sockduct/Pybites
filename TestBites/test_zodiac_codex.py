from datetime import datetime
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zodiac import (
    Sign,
    _get_month_int,
    get_sign_by_date,
    get_sign_with_most_famous_people,
    get_signs,
    signs_are_mutually_compatible,
)


@pytest.fixture
def raw_data():
    return [
        {
            "name": "Aries",
            "compatibility": ["Leo", "Sagittarius"],
            "famous_people": ["A", "B", "C"],
            "sun_dates": ["March 21", "April 19"],
        },
        {
            "name": "Taurus",
            "compatibility": ["Virgo", "Capricorn"],
            "famous_people": ["D"],
            "sun_dates": ["April 20", "May 20"],
        },
    ]


@pytest.fixture
def signs():
    return [
        Sign(
            name="Aries",
            compatibility=["Leo", "Sagittarius"],
            famous_people=["A", "B", "C"],
            sun_dates=["March 21", "April 19"],
        ),
        Sign(
            name="Taurus",
            compatibility=["Virgo", "Capricorn"],
            famous_people=["D"],
            sun_dates=["April 20", "May 20"],
        ),
        Sign(
            name="Leo",
            compatibility=["Aries"],
            famous_people=["E", "F"],
            sun_dates=["July 23", "August 22"],
        ),
        Sign(
            name="Pisces",
            compatibility=["Cancer", "Scorpio"],
            famous_people=["G"],
            sun_dates=["February 19", "March 20"],
        ),
    ]


def test_get_signs_returns_sign_namedtuples_in_order(raw_data):
    result = get_signs(raw_data)

    assert result == [
        Sign("Aries", ["Leo", "Sagittarius"], ["A", "B", "C"], ["March 21", "April 19"]),
        Sign("Taurus", ["Virgo", "Capricorn"], ["D"], ["April 20", "May 20"]),
    ]


def test_get_signs_returns_empty_list_for_empty_input():
    assert get_signs([]) == []


def test_get_signs_raises_keyerror_for_missing_required_field():
    incomplete = [{"name": "Aries"}]

    with pytest.raises(KeyError):
        get_signs(incomplete)


def test_get_sign_with_most_famous_people_returns_name_and_count(signs):
    assert get_sign_with_most_famous_people(signs) == ("Aries", 3)


def test_get_sign_with_most_famous_people_tie_returns_first_max():
    tie_signs = [
        Sign("One", [], ["A", "B"], ["January 1", "January 2"]),
        Sign("Two", [], ["C", "D"], ["January 3", "January 4"]),
    ]

    assert get_sign_with_most_famous_people(tie_signs) == ("One", 2)


def test_get_sign_with_most_famous_people_raises_on_empty_input():
    with pytest.raises(ValueError):
        get_sign_with_most_famous_people([])


def test_signs_are_mutually_compatible_returns_true_for_bidirectional_match(signs):
    assert signs_are_mutually_compatible(signs, "Aries", "Leo") is True


def test_signs_are_mutually_compatible_returns_false_for_non_match(signs):
    assert signs_are_mutually_compatible(signs, "Aries", "Taurus") is False


def test_signs_are_mutually_compatible_returns_false_when_sign_missing(signs):
    assert signs_are_mutually_compatible(signs, "Aries", "Unknown") is False


def test_signs_are_mutually_compatible_depends_on_iteration_order():
    asymmetric = [
        Sign("Alpha", ["Beta"], [], ["January 1", "January 2"]),
        Sign("Beta", [], [], ["January 3", "January 4"]),
    ]
    reversed_asymmetric = list(reversed(asymmetric))

    assert signs_are_mutually_compatible(asymmetric, "Alpha", "Beta") is False
    assert signs_are_mutually_compatible(reversed_asymmetric, "Alpha", "Beta") is True


def test_get_month_int_supports_abbreviation_and_full_name():
    assert _get_month_int("Jan") == 1
    assert _get_month_int("January") == 1


def test_get_month_int_raises_keyerror_for_invalid_month():
    with pytest.raises(KeyError):
        _get_month_int("NotAMonth")


def test_get_sign_by_date_returns_sign_for_start_boundary(signs):
    assert get_sign_by_date(signs, datetime(2024, 3, 21)) == "Aries"


def test_get_sign_by_date_returns_sign_for_end_boundary(signs):
    assert get_sign_by_date(signs, datetime(2024, 4, 19)) == "Aries"


def test_get_sign_by_date_returns_sign_for_middle_of_range(signs):
    assert get_sign_by_date(signs, datetime(2024, 5, 1)) == "Taurus"


def test_get_sign_by_date_handles_cross_month_end_of_pisces(signs):
    assert get_sign_by_date(signs, datetime(2024, 3, 20)) == "Pisces"


def test_get_sign_by_date_raises_assertion_error_when_no_sign_matches():
    # January date does not match any provided sign ranges in this custom dataset.
    custom = [
        Sign("Aries", [], [], ["March 21", "April 19"]),
        Sign("Taurus", [], [], ["April 20", "May 20"]),
    ]

    with pytest.raises(AssertionError):
        get_sign_by_date(custom, datetime(2024, 1, 1))
