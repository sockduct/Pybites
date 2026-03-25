#! /usr/bin/env python3.13
'''
Complete get_misssing_dates that takes an (unordered) sequence of datetime.date
objects. It should determine what the start and end date of this sequence is and
return the missing dates.

Here is an example (horizontal scroll code below):
>>> from datetime import date
>>> from missing_dates import get_misssing_dates
>>> date_range = [date(year=2019, month=2, day=n) for n in range(1, 11, 2)]
>>> date_range
[datetime.date(2019, 2, 1), datetime.date(2019, 2, 3),
 datetime.date(2019, 2, 5), datetime.date(2019, 2, 7), datetime.date(2019, 2, 9)
]

# our function returns the missing dates
# = the ones that were not generated in the preceding code
>>> sorted(get_misssing_dates(date_range))
[datetime.date(2019, 2, 2), datetime.date(2019, 2, 4),
 datetime.date(2019, 2, 6), datetime.date(2019, 2, 8)]

Some modules make this fairly easy (hint hint).

Thanks @shravankumar147 for sharing this idea on Twitter last week :)

Good luck and keep calm and code in Python!
'''


from collections import Counter
from datetime import date
from itertools import pairwise
from pprint import pformat

from dateutil.rrule import rrule, DAILY, MONTHLY
try:
    import pandas
except ImportError:
    pandas = None  # type: ignore[assignment]


def guess_freq(dates: list[date]) -> str|int:
    ordered = sorted(dates)
    interval = Counter(dt2 - dt1 for dt1, dt2 in pairwise(ordered)).most_common()[0][0]
    match days := interval.days:
        case days if 1 <= days <= 2:
            return DAILY
        case 7:
            return 'WEEKLY'
        case days if 28 <= days <= 31 or 56 <= days <= 62:
            return MONTHLY
        case days if 89 <= days <= 92:
            return 'QUARTERLY'
        case days if 365 <= days <= 366:
            return 'YEARLY'
        case _:
            return f'EVERY {days} DAYS'


def get_missing_dates(dates: list[date]) -> list[date]:
    """Receives a range of dates and returns a sequence
       of missing datetime.date objects (no worries about order).

       You can assume that the first and last date of the
       range is always present (assumption made in tests).

       See the Bite description and tests for example outputs.
    """
    if pandas:
        df = pandas.DataFrame(index=pandas.to_datetime(dates))
        return list(pandas.date_range(start=df.index.min(), end=df.index.max()).difference(df.index))
    else:
        start, end = min(dates), max(dates)
        # Just assume DAILY:
        expected = {dt.date() for dt in rrule(freq=DAILY, dtstart=start, until=end)}
        return sorted(expected - set(dates))


if __name__ == '__main__':
    date_range = [date(year=2019, month=2, day=n) for n in range(1, 11, 2)]
    print(f'Date range:\n{pformat(date_range)}\n'
          f'Missing dates:\n{pformat(get_missing_dates(date_range))}')
