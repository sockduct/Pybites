#! /usr/bin/env python3.13
'''
Doing a #100DaysOfCode can be challenging, and some of it is because you
dedicate to do it on workdays AND during weekends.

PyBites coding to the rescue. In this Bite you plan your next 100 days excluding
weekends.

Complete get_hundred_weekdays that takes a start_date which defaults to the
TODAY constant.

Read up on the awesome dateutil module and try to use it to generate a list of
100 weekdays from start_date. By completion you would have a cool new snippet
for your coding arsenal :) - good luck and enjoy the ride!
'''


from datetime import date
from pprint import pprint

from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR


TODAY = date(year=2018, month=11, day=29)


def get_hundred_weekdays(start_date: date=TODAY) -> list[date]:
    """Return a list of hundred date objects starting from
       start_date up till 100 weekdays later, so +100 days
       skipping Saturdays and Sundays"""
    return [
        dt.date()
        for dt in rrule(freq=DAILY, count=100, byweekday=(MO, TU, WE, TH, FR), dtstart=start_date)
    ]


if __name__ == '__main__':
    pprint(get_hundred_weekdays())
