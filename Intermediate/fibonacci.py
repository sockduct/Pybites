#! /usr/bin/env python3.13
'''
In this Bite you will learn about memoization: In computing, memoization or
memoisation is an optimization technique used primarily to speed up computer
programs by storing the results of expensive function calls and returning the
cached result when the same inputs occur again.

In Python you can implement this technique using the functools.cache decorator.

First write a simple fibonacci sequence calculator called cached_fib. It takes
an argument n and returns the sum of the previous two values in the sequence (or
the nth value of the Fibonacci sequence), so:

When n is 0, its fib value is n : fib(0) = 0
When n is 1, its fib value is n : fib(1) = 1
When n is 2, you add fib(1) and fib(0) : fib(2) = (1 + 0) = 1
When n is 3, you add fib(2) and fib(1) : fib(3) = (1 + 1) = 2
When n is 4, you add fib(3) and fib(2) : fib(4) = (2 + 1) = 3
When n is 5, you add fib(4) and fib(3) : fib(5) = (3 + 2) = 5
When n is 6, you add fib(5) and fib(4) : fib(6) = (5 + 3) = 8

The first test checks you return the correct result.

Next you speed it up using @cache. The second test checks if your implementation
is indeed faster than a classic fibonacci we wrote. As the fibonacci code is
part of the spec we've hidden the tests to not give away too much.
'''


from functools import cache


@cache
def cached_fib(n: int) -> int:
    if n < 0:
        raise ValueError('fibonacci number not defined for negative numbers!')
    elif n < 2:
        return n
    else:
        return cached_fib(n - 1) + cached_fib(n - 2)


if __name__ == '__main__':
    print(cached_fib(10))
