#! /usr/bin/env python3.13
'''
Goal:  Improve performance of supplied 5 function names ending with "_fast":
* Use better data structure
* Use better techniques
* May need to change function return type

Note:
* bisect would be a candidate for contains_fast but we think set (or dict) is
  the best way so this is the only function with a different input argument type
  for the fast equivalent (type casting was too expensive)
* The tests ensure that the fast functions:
  A. return the same result
  B. are indeed faster
'''


from collections import deque
from collections.abc import Callable
from functools import wraps
from time import time
from typing import Any, Generator, TypeVar, cast


Func = TypeVar('Func', bound=Callable[..., Any])
TimeFunc = TypeVar('TimeFunc', bound=Callable[..., tuple[float, Any]])


def timing(func: Func) -> Func:
    """A simple timer decorator to print the elapsed time of
       the execution of the function it wraps.
       Returns (timing, result) tuple"""
    @wraps(func)
    def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> tuple[float, Any]:
        start = time()
        result = func(*args, **kwargs)
        end = time()
        duration = end - start
        print(f'Elapsed time {func.__name__}: {duration}')
        return duration, result
    return cast(Func, wrapper)


@timing
def contains(sequence: list[int], num: int) -> bool:
    for n in sequence:
        if n == num:
            return True
    return False


@timing
def contains_fast(sequence: set[int], num: int) -> bool:
    return num in sequence


@timing
def ordered_list_max(sequence: list[int]) -> int:
    return max(sequence)


@timing
def ordered_list_max_fast(sequence: list[int]) -> int:
    # If assume ascending order:
    # return sequence[-1]
    return max(sequence[0], sequence[-1])


@timing
def list_concat(sequence: list[str]) -> str:
    bigstr = ''
    for i in sequence:
        bigstr += str(i)
    return bigstr


@timing
def list_concat_fast(sequence: list[str]) -> str:
    return ''.join(sequence)


@timing
def list_inserts(n: int) -> list[int]:
    lst: list[int] = []
    for i in range(n):
        lst.insert(0, i)
    return lst


@timing
def list_inserts_fast(n: int) -> deque[int]:
    '''
    Alternatives:
    return list(range(n - 1, -1, -1))

    deq: deque[int] = deque()
    for i in range(n):
        deq.appendleft(i)
    return deq
    '''
    return deque(reversed(range(n)))


@timing
def list_creation(n: int) -> list[int]:
    lst = []
    for i in range(n):
        lst.append(i)
    return lst


@timing
def list_creation_fast(n: int) -> Generator[int, None, None]:
    '''
    Alternative:
    return range(n)  # Change return type to range

    Using below to stick with proposed return type:
    '''
    return (i for i in range(n))
