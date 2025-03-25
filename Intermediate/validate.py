#! /usr/bin/env python3.13
'''
Let's get some more practice with decorators ... in this Bite you will write a
decorator that checks if input arguments (*args) are positive integers.

You would use *args when you're not sure how many arguments might be passed to
your function, i.e. it allows you pass an arbitrary number of arguments to your
function.

If one or more of the passed in args are not of type int, it throws a TypeError,
if it is an int but < 0, it throws a ValueError.

That's it! Wrap it in a nice decorator and the tests will validate your code.
Have fun!
'''


from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar


P = ParamSpec('P')
R = TypeVar('R')


def int_args(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def int_validate(*args: P.args, **kwargs: P.kwargs) -> R:
        for arg in args:
            if not isinstance(arg, int):
                raise TypeError(f'Expected positive integer, got non-integer type "{arg}".')
            elif arg < 0:
                raise ValueError(f'Expected positive integer, got negative value "{arg}".')
        return func(*args, **kwargs)

    return int_validate


@int_args
def int_test(*args: int) -> None:
    print('inside int_test...')


if __name__ == '__main__':
    for args in [(1, 2), (1.1, 5), (-1, 0), ('bad', 1)]:
        print(f'Invoking function with args:  {args}:')
        try:
            # Testing invalid values - OK:
            int_test(*args)  # type: ignore
        except (TypeError, ValueError) as err:
            print(err)
