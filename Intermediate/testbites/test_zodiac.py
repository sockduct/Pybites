from datetime import datetime
from itertools import combinations
import json
import os
from pathlib import Path
from typing import NamedTuple, TypedDict
from urllib.request import urlretrieve

import pytest

from zodiac import (get_signs, get_sign_with_most_famous_people,
                    signs_are_mutually_compatible, get_sign_by_date, Sign)

# original source: https://zodiacal.herokuapp.com/api
URL = "https://bites-data.s3.us-east-2.amazonaws.com/zodiac.json"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, "zodiac.json")


class Data(TypedDict):
    __v: int
    _id: str
    bad_traits: list[str]
    body_parts: list[str]
    cardinality: str
    element: str
    famous_people: list[str]
    favorites: list[str]
    good_traits: list[str]
    hates: list[str]
    how_to_spot: list[str]
    keywords: list[str]
    mental_traits: list[str]
    name: str
    physical_traits: list[str]
    ruling_planet: list[str]
    secret_wish: list[str]
    sun_dates: list[str]
    symbol: str
    vibe: str


@pytest.fixture(scope='module')
def signs() -> list[Sign]:
    if not PATH.exists():
        urlretrieve(URL, PATH)
    with open(PATH) as f:
        data = json.loads(f.read())
    return get_signs(data)

# write your pytest code here ...
def test_get_signs(signs: list[Sign]) -> None:
    '''get_signs -> list[Sign]'''
    assert len(signs) == 12
    assert {
        'Aquarius', 'Aries', 'Cancer', 'Capricorn', 'Gemini', 'Leo',
        'Libra', 'Pisces', 'Sagittarius', 'Scorpio', 'Taurus', 'Virgo'
    } == {sign.name for sign in signs}

def test_get_sign_with_most_famous_people(signs: list[Sign]) -> None:
    '''get_sign_with_most_famous_people -> tuple[str, int]'''
    assert test_get_sign_with_most_famous_people(signs) == ('Scorpio', 35)

def test_signs_are_mutually_compatible(signs: list[Sign]) -> None:
    '''signs_are_mutually_compatible -> bool'''
    combos = list(combinations([s.name for s in signs], 2))
    assert len(combos) == 66
    assert sum(signs_are_mutually_compatible(signs, t[0], t[1]) for t in combos) == 10

def test_get_sign_by_date(signs: list[Sign]) -> None:
    '''get_sign_by_date -> str'''
    assert get_sign_by_date(signs, datetime(2026, 3, 7)) == 'Pisces'
