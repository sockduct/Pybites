#! /usr/bin/env python3.13
'''
Another real world use case. When we added notifications to our learning paths,
we gave the user the option to receive x number of Bites every y number of days.
Based on these two input parameters, code up the gen_bite_planning generator
that returns date objects for the notifications.

With the default set to notify one Bite a day, the script using your
gen_bite_planning generator would output the following:
>>> from datetime import date
>>> from notifications import gen_bite_planning
>>> today = date.today()
>>> today
datetime.date(2019, 8, 25)
>>> gen = gen_bite_planning(num_bites=1, num_days=1, start_date=today)
>>> for _ in range(10):
...     next(gen)
...
datetime.date(2019, 8, 26)
datetime.date(2019, 8, 27)
datetime.date(2019, 8, 28)
datetime.date(2019, 8, 29)
datetime.date(2019, 8, 30)
datetime.date(2019, 8, 31)
datetime.date(2019, 9, 1)
datetime.date(2019, 9, 2)
datetime.date(2019, 9, 3)
datetime.date(2019, 9, 4)

If the user decides to do 2 Bites every 3 days, the generator would output the following:
>>> gen = gen_bite_planning(num_bites=2, num_days=3, start_date=today)
>>> for _ in range(10):
...     next(gen)
...
datetime.date(2019, 8, 28)
datetime.date(2019, 8, 28)
datetime.date(2019, 8, 31)
datetime.date(2019, 8, 31)
datetime.date(2019, 9, 3)
datetime.date(2019, 9, 3)
datetime.date(2019, 9, 6)
datetime.date(2019, 9, 6)
datetime.date(2019, 9, 9)
datetime.date(2019, 9, 9)

And a Bite every other day would return this:
>>> gen = gen_bite_planning(num_bites=1, num_days=2, start_date=today)
>>> for _ in range(10):
...     next(gen)
...
datetime.date(2019, 8, 27)
datetime.date(2019, 8, 29)
datetime.date(2019, 8, 31)
datetime.date(2019, 9, 2)
datetime.date(2019, 9, 4)
datetime.date(2019, 9, 6)
datetime.date(2019, 9, 8)
datetime.date(2019, 9, 10)
datetime.date(2019, 9, 12)
datetime.date(2019, 9, 14)
'''


from collections.abc import Iterator
from datetime import date, timedelta


TODAY = date.today()


def gen_bite_planning(num_bites: int=1, num_days: int=1, start_date: date=TODAY) -> Iterator[date]:
    while True:
        start_date += timedelta(days=num_days)
        for _ in range(num_bites):
            yield start_date


if __name__ == '__main__':
    today = date(2019, 8, 25)
    for params in [(1, 1, today), (2, 3, today), (1, 2, today)]:
        gen = gen_bite_planning(*params)
        print(f'gen_bite_planning({", ".join(str(p) for p in params)}):')
        for i in range(1, 11):
            print(f'{i:>2}: {next(gen)}')
        print()
