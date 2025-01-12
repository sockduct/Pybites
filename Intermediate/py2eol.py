#! /usr/bin/env python3.13

from datetime import datetime


# https://pythonclock.org/
PY2_DEATH_DT = datetime(year=2020, month=1, day=1)
BITE_CREATED_DT = datetime.strptime('2018-02-26 23:24:04', '%Y-%m-%d %H:%M:%S')
EARTH_TO_MILLER_RATIO = 7 * 365 * 24


def get_py2_earth_hours_left(start_date: datetime=BITE_CREATED_DT) -> float:
    return (PY2_DEATH_DT - start_date).total_seconds()/3600


def py2_earth_hours_left(start_date: datetime=BITE_CREATED_DT) -> float:
    """Return how many hours, rounded to 2 decimals, Python 2 has
       left on Planet Earth (calculated from start_date)"""
    return round(get_py2_earth_hours_left(start_date), 2)


def py2_miller_min_left(start_date: datetime=BITE_CREATED_DT) -> float:
    """Return how many minutes, rounded to 2 decimals, Python 2 has
       left on Planet Miller (calculated from start_date)"""
    miller_hours = get_py2_earth_hours_left(start_date)/EARTH_TO_MILLER_RATIO
    return round(miller_hours * 60, 2)


if __name__ == '__main__':
    print(f'{py2_earth_hours_left():,.2f}')
    print(f'{py2_miller_min_left():,.2f}')
