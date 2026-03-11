from collections.abc import Callable
from datetime import date, datetime
from itertools import combinations
import json
import os
from pathlib import Path
from urllib.request import urlretrieve

import pytest

from zodiac import (get_signs, get_sign_with_most_famous_people,
                    signs_are_mutually_compatible, get_sign_by_date, Sign)

# original source: https://zodiacal.herokuapp.com/api
URL = "https://bites-data.s3.us-east-2.amazonaws.com/zodiac.json"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, "zodiac.json")


@pytest.fixture(scope='module')
def signs() -> list[Sign]:
    if not PATH.exists():
        urlretrieve(URL, PATH)
    with open(PATH, encoding='utf-8') as f:
        data = json.load(f)
    return get_signs(data)

# write your pytest code here ...
def _get_dt_pair(dts: list[str]) -> tuple[date, date]:
    year = 2026
    gdt: Callable[[str], date] = lambda d: datetime.strptime(f'{d} {year}', '%B %d %Y').date()
    dt2 = gdt(dts[1])
    if dts[0].startswith('Dec'):
        year = 2025
    dt1 = gdt(dts[0])
    return dt1, dt2

def test_get_signs(signs: list[Sign]) -> None:
    '''get_signs -> list[Sign]'''
    # Could also test type:
    # assert type(signs) == list
    assert len(signs) == 12
    assert {
        'Aquarius', 'Aries', 'Cancer', 'Capricorn', 'Gemini', 'Leo',
        'Libra', 'Pisces', 'Sagittarius', 'Scorpio', 'Taurus', 'Virgo'
    } == {sign.name for sign in signs}
    sdts = [_get_dt_pair(sign.sun_dates) for sign in signs]
    YEAR = 365
    assert sum((dt[1] - dt[0]).days for dt in sdts) + 12 == YEAR

'''
# Could also test sign type:
def test_sign_namedtuple(signs):
    sign = signs[0]
    assert str(sign).startswith('Sign')
'''

def test_get_sign_with_most_famous_people(signs: list[Sign]) -> None:
    '''get_sign_with_most_famous_people -> tuple[str, int]'''
    '''
    # Check for multiple candidates:
    top_signs = ('Scorpio', 35), ('Capricorn', 35)
    assert get_sign_with_most_famous_people(signs) in top_signs
    '''
    assert get_sign_with_most_famous_people(signs) == ('Scorpio', 35)

def test_signs_are_mutually_compatible(signs: list[Sign]) -> None:
    '''signs_are_mutually_compatible -> bool'''
    combos = list(combinations([s.name for s in signs], 2))
    assert len(combos) == 66
    assert sum(signs_are_mutually_compatible(signs, t[0], t[1]) for t in combos) == 10
'''
# Another take on the above:
@pytest.mark.parametrize("sign1, sign2, expected", [
    ("Aries", "Taurus", False),
    ("Aries", "Gemini", True),
    ("Taurus", "Gemini", False),
    ("Taurus", "Cancer", True),
    ("Taurus", "Leo", False),
    ("Gemini", "Cancer", False),
    ("Gemini", "Libra", True),
    ("Cancer", "Leo", False),
    ("Cancer", "Scorpio", True),
    ("Taurus", "Pisces", True),
    ("Pisces", "Taurus", True),
])
def test_signs_are_mutually_compatible(sign1, sign2, expected, signs):
    assert signs_are_mutually_compatible(signs, sign1, sign2) == expected
    # wow mutpy you can be nasty! ;)
    assert signs_are_mutually_compatible(signs, sign2, sign1) == expected
'''

def test_get_sign_by_date(signs: list[Sign]) -> None:
    '''get_sign_by_date -> str'''
    assert get_sign_by_date(signs, datetime(2026, 3, 7)) == 'Pisces'
'''
# Another take on the above:
@pytest.mark.parametrize("month, day, expected", [
    (3, 21, 'Aries'),
    (4, 19, 'Aries'),
    (4, 20, 'Taurus'),
    (5, 1, 'Taurus'),
    (5, 20, 'Taurus'),
    (5, 21, 'Gemini'),
    (6, 20, 'Gemini'),
    (6, 21, 'Cancer'),
    (7, 1, 'Cancer'),
    (7, 22, 'Cancer'),
    (8, 22, 'Leo'),
    (8, 23, 'Virgo'),
    (9, 1, 'Virgo'),
    (9, 22, 'Virgo'),
    (9, 23, 'Libra'),
    (10, 22, 'Libra'),
    (10, 23, 'Scorpio'),
    (11, 21, 'Scorpio'),
    (11, 22, 'Sagittarius'),
    (12, 1, 'Sagittarius'),
    (12, 21, 'Sagittarius'),
    (12, 22, 'Capricorn'),
    (1, 19, 'Capricorn'),
    (1, 20, 'Aquarius'),
    (2, 18, 'Aquarius'),
    (2, 19, 'Pisces'),
    (3, 1, 'Pisces'),
    (3, 20, 'Pisces'),
])
def test_get_sign_by_date(signs, month, day, expected):
    actual = get_sign_by_date(signs, datetime(year=2019, month=month, day=day))
    assert actual == expected
'''
