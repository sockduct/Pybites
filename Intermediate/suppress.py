#! /usr/bin/env python3.13
'''
Ever wanted to suppress an exception? Check out Python's contextlib module.

In this Bite you refactor sum_numbers which has some nested try/except
statements. Use suppress to make this logic cleaner/ more readable. Have fun and
keep calm and code in Python!
'''


from collections.abc import Iterator
from contextlib import suppress


type Number = int|float


def sum_numbers(numbers: list[Number]) -> Iterator[Number]:
    """This generator divides each number by its consecutive number.
       So if it gets passed in [4, 2, 1] it yields 4/2 and 2/1.
       It ignores ZeroDivisionError and TypeError exceptions (latter happens
       when a string or other non-numeric data type is in numbers)

       Task: use contextlib's suppress twice to make the code below more concise.
    """
    for i, j in zip(numbers, numbers[1:]):
        # replace the block below
        with suppress(TypeError, ZeroDivisionError):
            yield i/j
