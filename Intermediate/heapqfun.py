#! /usr/bin/env python3.13


from datetime import datetime
import heapq


numbers = [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6]
dates = [datetime(2018, 1, 23, 0, 0),
         datetime(2017, 12, 19, 0, 0),
         datetime(2017, 10, 15, 0, 0),
         datetime(2019, 2, 27, 0, 0),
         datetime(2017, 3, 29, 0, 0),
         datetime(2018, 8, 11, 0, 0),
         datetime(2018, 5, 3, 0, 0),
         datetime(2018, 12, 19, 0, 0),
         datetime(2018, 11, 19, 0, 0),
         datetime(2017, 7, 7, 0, 0)]
# static (outdated) copy of:
# https://www.forbes.com/celebrities/list
earnings_mln: list[dict[str, str|int|float]] = [
    {'name': 'Kevin Durant', 'earnings': 60.6},
    {'name': 'Adele', 'earnings': 69},
    {'name': 'Lionel Messi', 'earnings': 80},
    {'name': 'J.K. Rowling', 'earnings': 95},
    {'name': 'Elton John', 'earnings': 60},
    {'name': 'Chris Rock', 'earnings': 57},
    {'name': 'Justin Bieber', 'earnings': 83.5},
    {'name': 'Cristiano Ronaldo', 'earnings': 93},
    {'name': 'Beyoncé Knowles', 'earnings': 105},
    {'name': 'Jackie Chan', 'earnings': 49},
]


def get_largest_number(numbers: list[int], n: int=3) -> list[int]:
    return heapq.nlargest(n, numbers)


def get_latest_dates(dates: list[datetime], n: int=3) -> list[datetime]:
    return heapq.nlargest(n, dates)


def get_highest_earnings(earnings_mln: list[dict[str, str|int|float]], n: int=3
                         ) -> list[dict[str, str|int|float]]:
    return heapq.nlargest(n, earnings_mln, key=lambda e: e['earnings'])


if __name__ == '__main__':
    print(get_largest_number(numbers))
    print(get_latest_dates(dates))
    print(get_highest_earnings(earnings_mln))
