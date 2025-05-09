#! /usr/bin/env python3.13
'''
For this Bite you are asked to start working on a reading goal feature for a
books app.

Code up get_number_books_read that takes a yearly # books to read int and then
calculates the amount of books user should have read based on the at_date
argument which defaults to NOW.

So if the goal is 52, and we call this function week 11, it should return 11.
If the goal is 100 and we call this function in week 47 the function should
return 90 (47/52*100), rounding to int.

Some more examples:
>>> get_number_books_read(100, 'Sunday, March 25th, 2019')
25
>>> get_number_books_read(52, 'Sunday, March 18th, 2019')
12
>>> get_number_books_read(52, '5-20-2018')
Traceback (most recent call last):
  File "", line 1, in
  File "/Users/bbelderbos/code/bitesofpy/186/books.py", line 20, in get_number_books_read
    raise ValueError('Should have positive goal and future date')
ValueError: Should have positive goal and future date

Check the docstring, comments and tests for more guidance.

For simplicity you can assume that a year has 52 weeks
(hence WEEKS_PER_YEAR = 52).

Hint: to get the week of the year, look into isocalendar.

Keep calm and code in Python! 🐍 🔥
'''


from datetime import datetime

from dateutil.parser import parse

# work with a static date for tests, real use = datetime.now()
NOW = datetime(2019, 3, 17, 16, 28, 42, 966663)
WEEKS_PER_YEAR = 52


def get_number_books_read(books_per_year_goal: int,
                          at_date: datetime|str=NOW) -> int:
    """Based on books_per_year_goal and at_date, return the
       number of books that should have been read.
       If books_per_year_goal negative or 0, or at_date is in the
       past, raise a ValueError."""
    '''
    TODOs:
    1. use dateutil's parse to convert at_date into a datetime object
    2. check books_per_year_goal and at_date and raise a ValueError if goal <= 0
       or at_date in the past (< NOW)
    3. check the offset of at_date in the year ("week of the year" - e.g.
       whatweekisit.com) and based on the books_per_year_goal, calculate the
       number of books that should have been read / completed
    '''
    # Sanity check:
    if at_date is None:
        at_date = NOW
    elif isinstance(at_date, str):
        at_date = parse(at_date)
    elif not isinstance(at_date, datetime):
        raise TypeError(f'at_date must be a str or datetime, not {type(at_date)}')

    if books_per_year_goal <= 0 or at_date < NOW:
        raise ValueError(
            f'books/year goal must be > 0 and date must be after {NOW:%B %dth, %Y}'
        )

    current_week = at_date.isocalendar().week

    return int(books_per_year_goal * current_week/WEEKS_PER_YEAR)


if __name__ == '__main__':
    for books, dt, expected in (
        (100, 'Sunday, March 25th, 2019', 25),
        (52, 'Sunday, March 18th, 2019', 12),
        (52, '5-20-2018', 'ValueError')
    ):
        try:
            print(f'Goal: {books}, Date: {dt} => ', end='')
            result = get_number_books_read(books, dt)
            print(result, end='')
        except ValueError as err:
            print(f'Error: {err}', end='')
        finally:
            print(f' (expected: {expected})')
