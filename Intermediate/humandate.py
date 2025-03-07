#! /usr/bin/env python3.13
'''
Humanize datetimes - convert timedelta output into human readable form
- If the date passed into pretty_date is <= 2 days ago return the pretty date
  string - you can use TIME_OFFSETS for this
- If the date passed in is older than that, return the date in the format
  month/day/year, 2 digits each, e.g. 05/19/18
- If a non datetime object is passed into the pretty_date function, raise a
  ValueError.
'''


from datetime import datetime, timedelta
from typing import Callable, NamedTuple


# Types:
class TimeOffset(NamedTuple):
    offset: int
    date_str:  str
    divider:  int|None


NOW = datetime.now()
MINUTE, HOUR, DAY = 60, 60*60, 24*60*60
TIME_OFFSETS = (
    TimeOffset(10, 'just now', None),
    TimeOffset(MINUTE, '{} seconds ago', None),
    TimeOffset(2*MINUTE, 'a minute ago', None),
    TimeOffset(HOUR, '{} minutes ago', MINUTE),
    TimeOffset(2*HOUR, 'an hour ago', None),
    TimeOffset(DAY, '{} hours ago', HOUR),
    TimeOffset(2*DAY, 'yesterday', None),
)


def pretty_date(date: datetime) -> str:
    """Receives a datetime object and converts/returns a readable string
       using TIME_OFFSETS"""
    if not isinstance(date, datetime):
        raise ValueError(f'Expected datetime, got {date.__class__.__name__}')
    if date > NOW:
        raise ValueError(f'Error:  {date} is in the future!')

    offset = int((NOW - date).total_seconds())
    for time_offset in TIME_OFFSETS:
        if offset < time_offset.offset:
            new_offset = offset//time_offset.divider if time_offset.divider else offset
            return time_offset.date_str.format(new_offset)

    return date.strftime('%m/%d/%y')


if __name__ == '__main__':
    timeval: Callable[[int], datetime] = lambda val: NOW - timedelta(seconds=val)
    for val in (timeval(9), timeval(59), timeval(119), timeval(3599), timeval(7199),
                timeval(86399), timeval(172799), timeval(172800), timeval(172801),
                'invalid', 123, timeval(-5)):
        try:
            # Note:  We know we're sending some illegal types but on purpose.
            print(f'{val} => {pretty_date(val)}')  # type: ignore
        except ValueError as err:
            print(f'{val}:  {err}')
