#! /usr/bin/env python3.13
'''
Let's do another datetime processing Bite. Complete add_todo below that converts
time units to future timestamps.

Here is how it works with given default start_time of NOW:
>>> from timer import add_todo, NOW
>>> str(NOW)
'2019-02-06 22:00:00'
>>> add_todo("11h 10m", "Wash my car")
'Wash my car @ 2019-02-07 09:10:00'
>>> add_todo("30d", "Code a Bite")
'Code a Bite @ 2019-03-08 22:00:00'
>>> add_todo("5m 3s", "Go to Bed")
'Go to Bed @ 2019-02-06 22:05:03'

See the docstring and tests for more output examples. Good luck and code more
Python!
'''


from datetime import datetime, timedelta
import re


NOW = datetime(year=2019, month=2, day=6, hour=22, minute=0, second=0)


def add_todo(delay_time: str, task: str,
             start_time: datetime=NOW) -> str:
    """
    Add a todo list item in the future with a delay time.

    Parse out the time unit from the passed in delay_time str:
    - 30d = 30 days
    - 1h 10m = 1 hour and 10 min
    - 5m 3s = 5 min and 3 seconds
    - 45 or 45s = 45 seconds

    Return the task and planned time which is calculated from
    provided start_time (here default = NOW):
    >>> add_todo("1h 10m", "Wash my car")
    >>> "Wash my car @ 2019-02-06 23:10:00"
    """
    pattern = r'(?P<days>\d+d)?\s*(?P<hours>\d+h)?\s*(?P<minutes>\d+m)?\s*(?P<seconds>\d+s?)?'
    result = re.search(pattern, delay_time, re.IGNORECASE)
    assert result is not None  # Know it's safe because using ?P<NAME> for each name
    units = {
        key: int(value.strip('dhms')) if value else 0
        for key, value in result.groupdict().items()
    }

    due_time = start_time + timedelta(**units)
    return f'{task} @ {due_time:%Y-%m-%d %H:%M:%S}'


if __name__ == '__main__':
    for delay_time, task in (
        ("11h 10m", "Wash my car"),
        ("30d", "Code a Bite"),
        ("5m 3s", "Go to Bed"),
    ):
        print(f'{delay_time=}, {task=} => {add_todo(delay_time, task)}')
