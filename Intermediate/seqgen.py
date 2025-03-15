#! /usr/bin/env python3.13
'''
Write a generator that produces the sequence:
[1, 'A', 2, 'B', 3, 'C', ... 'X', 25, 'Y', 26, 'Z'] infinitely

So once you hit Z you start at 1 again, etc.
Maybe itertools can help you here?
'''


from itertools import cycle
from string import ascii_uppercase
from typing import Generator


def sequence_generator() -> Generator[int|str]:
    for number, letter in cycle(enumerate(ascii_uppercase, 1)):
        yield number
        yield letter


if __name__ == '__main__':
    for val in sequence_generator():
        print(f'{val} ', end='')
        if val == 11:
            break
