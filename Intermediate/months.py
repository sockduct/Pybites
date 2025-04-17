#! /usr/bin/env python3.13
'''
Some more fun working with dates! In this Bite you will calculate the number of
months between the fixed START_DATE = date(2018, 11, 1) and the date you will
construct from the input arguments.

You should raise the proper exceptions and perform the proper upper rounding
based on the fact that >= 10 days in the datetime difference adds another month
to the counter.

Best to give you some examples of the expected results so check out the
docstring and tests, then start coding Python 💪. You probably want to use
dateutil.relativedelta for this one! Good luck!
'''


from datetime import date

from dateutil.relativedelta import relativedelta


START_DATE = date(2018, 11, 1)
MIN_DAYS_TO_COUNT_AS_MONTH = 10
MONTHS_PER_YEAR = 12


def calc_months_passed(year: int, month: int, day: int) -> int:
    """Construct a date object from the passed in arguments.
       If this fails due to bad inputs reraise the exception.
       Also if the new date is < START_DATE raise a ValueError.

       Then calculate how many months have passed since the
       START_DATE constant. We suggest using dateutil.relativedelta!

       One rule: if a new month is >= 10 (MIN_DAYS_TO_COUNT_AS_MONTH)
       days in, it counts as an extra month.

       For example:
       date(2018, 11, 10) = 9 days in => 0 months
       date(2018, 11, 11) = 10 days in => 1 month
       date(2018, 12, 11) = 1 month + 10 days in => 2 months
       date(2019, 12, 11) = 1 year + 1 month + 10 days in => 14 months
       etc.

       See the tests for more examples.

       Return the number of months passed int.
    """
    dt = date(year=year, month=month, day=day)
    if dt < START_DATE:
        raise ValueError(f'Date ({dt}) before {START_DATE}')

    reldt = relativedelta(dt, START_DATE)

    months = reldt.years * MONTHS_PER_YEAR + reldt.months
    if reldt.days >= MIN_DAYS_TO_COUNT_AS_MONTH:
        months += 1

    # return f'{months} months' if months != 1 else f'{months} month'
    return months


if __name__ == '__main__':
    for test_date in (
        date(2018, 11, 10), # = 9 days in => 0 months
        date(2018, 11, 11), # = 10 days in => 1 month
        date(2018, 12, 11), # = 1 month + 10 days in => 2 months
        date(2019, 12, 11), # = 1 year + 1 month + 10 days in => 14 months
    ):
        print(
            f'Testing {test_date}:  '
            f'{calc_months_passed(test_date.year, test_date.month, test_date.day)}'
        )
