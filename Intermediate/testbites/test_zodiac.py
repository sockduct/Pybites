from datetime import datetime
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
def signs() -> list[Sign]
    if not PATH.exists():
        urlretrieve(URL, PATH)
    with open(PATH) as f:
        data = json.loads(f.read())
    return get_signs(data)

# write your pytest code here ...
def test_get_signs(signs: list[Sign]):
    assert len(signs) == 12
    assert {
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra',
        'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    } == {sign.name for sign in signs}
