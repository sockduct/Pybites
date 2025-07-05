#! /usr/bin/env python3.13
'''
It's the 12th of May 2019 when we write this so happy Mother's Day! In many
countries this special day is celebrated on the second Sunday of May. In this
Bite you will calculate which date this was / will be for year range 2014-2024.

Complete get_mothers_day_date which takes a year int argument and returns a date
object = the 2nd Sunday of May for that year. We use this table in our tests to
verify your code.
'''


from datetime import date, timedelta


def get_mothers_day_date(year: int, *, month: int=5, day: int=6, week: int=2) -> date:
    """Given the passed in year int, return the date Mother's Day
       is celebrated assuming it's the 2nd Sunday of May."""
    # Determine which day (Sunday - Saturday) 1st of the month is:
    '''
    Alternative solution:
    from dateutil.relativedelta import relativedelta, SU

    first_of_may = date(year=year, month=MAY, day=1)
    return first_of_may + relativedelta(weeks=1, weekday=SU)
    '''
    offset = day - date(year, month, 1).weekday()
    return date(year, month, 1) + timedelta(offset + 7 * (week - 1))


if __name__ == '__main__':
    for year in range(2014, 2026):
        print(f'{get_mothers_day_date(year)=}')
