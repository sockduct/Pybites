import calendar
from collections import namedtuple
from datetime import datetime
from operator import itemgetter
from typing import NamedTuple, TypedDict


class Data(TypedDict):
    __v: int
    _id: str
    bad_traits: list[str]
    body_parts: list[str]
    cardinality: str
    compatibility: list[str]
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


# Sign = namedtuple('Sign', 'name compatibility famous_people sun_dates')
class Sign(NamedTuple):
    name: str
    compatibility: list[str]
    famous_people: list[str]
    sun_dates: list[str]


### Temp to include private function:
__all__ = [
    'get_signs', 'get_sign_with_most_famous_people', 'signs_are_mutually_compatible',
    '_get_month_int', 'get_sign_by_date', 'Sign'
]
### End Temp


def get_signs(data: list[Data]) -> list[Sign]:
    ret = []
    for datum in data:
        name = datum['name']
        compatibility = datum['compatibility']
        famous_people = datum['famous_people']
        sun_dates = datum['sun_dates']
        sign = Sign(name, compatibility, famous_people, sun_dates)
        ret.append(sign)
    return ret


def get_sign_with_most_famous_people(signs: list[Sign]) -> tuple[str, int]:
    """Get the sign with the most famous people associated"""
    famous_people = [
        (s.name, len(s.famous_people)) for s in signs
    ]
    return max(famous_people, key=itemgetter(1))


def signs_are_mutually_compatible(signs: list[Sign], sign1: str, sign2: str) -> bool:
    """Given 2 signs return if they are compatible (compatibility field)"""
    ret = False
    for sign in signs:
        if sign.name == sign1:
            ret = sign2 in sign.compatibility
        elif sign.name == sign2:
            ret = sign1 in sign.compatibility
    return ret


def _get_month_int(month: str) -> int:
    month_mapping = {
        v: k for k, v in enumerate(calendar.month_abbr)
    }
    return int(month_mapping[month[:3]])


def get_sign_by_date(signs: list[Sign], date: datetime) -> str:
    """Given a date return the right sign (sun_dates field)"""
    month = date.month
    day = date.day

    for sign in signs:
        start, end = sign.sun_dates
        start_month, start_day = start.split()
        end_month, end_day = end.split()
        if(
            month == _get_month_int(start_month) and day >= int(start_day)
            or
            month == _get_month_int(end_month) and day <= int(end_day)
        ):
            return sign.name

    raise AssertionError('Either received invalid data or unhandled use case.')
