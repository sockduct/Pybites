#! /usr/bin/env python3.13
'''
In this Bite you will create a simple calculator. It takes a string of num1
operator num2 which you convert into its calculation returning its result.
Complete simple_calculator to that end supporting +, -, * and / ("true" division
so 2/3 = .66 rather than 0).

So passing '2 * 3' into the function it would return 6, '2 + 6' results in 8,
'-5 * -11' = 55 and lastly '1 / 5' = 0.20.

For any bad data passed into the function (e.g. a / 3, 2 * b, 1 ^ 2, etc), you
should raise a ValueError.

Good luck and have fun!
'''


from contextlib import suppress
import operator
from typing import cast


OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


def simple_calculator(calculation: str) -> int|float:
    """Receives 'calculation' and returns the calculated result,

       Examples - input -> output:
       '2 * 3' -> 6
       '2 + 6' -> 8

       Support +, -, * and /, use "true" division (so 2/3 is .66
       rather than 0)

       Make sure you convert both numbers to ints.
       If bad data is passed in, raise a ValueError.
    """
    '''
    match calculation.split():
        case [x, '+', y]:
            return int(x) + int(y)
        case [x, '-', y]:
            return int(x) - int(y)
        case [x, '*', y]:
            return int(x) * int(y)
        case [x, '/', y]:
            if y == '0':
                raise ValueError(f'Attempt to divide by 0:  {calculation}')
            return int(x) / int(y)
        case _:
            raise ValueError(f'Unexpected calculation:  {calculation}')
    '''
    # Better:
    try:
        num1, op, num2 = calculation.split()
        return cast(int|float, OPS[op](int(num1), int(num2)))
    except (KeyError, ValueError, ZeroDivisionError) as err:
        print(err)
        raise ValueError from err


if __name__ == '__main__':
    for test in ('2 * 3', '2 + 6', '2 / 3', 'a + b', 'c/d', '3 / 0', '1 ^ 5'):
        with suppress(ValueError, KeyError, ZeroDivisionError) as err:
            if err:
                print(err)
            print(f'{test} => {simple_calculator(test)}')
