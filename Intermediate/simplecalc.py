#! /usr/bin/env python3.13


import argparse
from functools import reduce
from math import prod
from operator import sub, truediv
from typing import Callable, TypedDict


class Operations(TypedDict):
   add: Callable[[list[float]], float]
   sub: Callable[[float, float], float]
   mul: Callable[[list[float]], float]
   div: Callable[[float, float], float]


operations: Operations = dict(add=sum, sub=sub, mul=prod, div=truediv)


def calculator(operation: str, numbers: list[float]) -> float:
    """TODO 1:
       Create a calculator that takes an operation and list of numbers.
       Perform the operation returning the result rounded to 2 decimals"""
    if operation not in operations:
        raise ValueError(f'Expected add/sub/mul/div, got "{operation}"')

    match operation:
        case 'sub' | 'div':
            res = reduce(operations[operation], numbers)
        case 'add' | 'mul':
            res = operations[operation](numbers)

    return round(res, 2)


def create_parser() -> argparse.ArgumentParser:
    """TODO 2:
       Create an ArgumentParser object:
       - have one operation argument,
       - have one or more integers that can be operated on.
       Returns a argparse.ArgumentParser object.

       Note that type=float times out here so do the casting in the calculator
       function above!"""
    parser = argparse.ArgumentParser(description='A simple calculator')
    parser.add_argument(
        '-a', '--add', action='extend', nargs='+', type=float, metavar='num',
        help='Sums numbers'
    )
    parser.add_argument(
        '-s', '--sub', action='extend', nargs='+', type=float, metavar='num',
        help='Subtracts numbers'
    )
    parser.add_argument(
        '-m', '--mul', action='extend', nargs='+', type=float, metavar='num',
        help='Multiplies numbers'
    )
    parser.add_argument(
        '-d', '--div', action='extend', nargs='+', type=float, metavar='num',
        help='Divides numbers'
    )

    return parser


def call_calculator(args: argparse.Namespace|None=None, stdout: bool=False) -> float|None:
    """Provided/done:
       Calls calculator with provided args object.
       If args are not provided get them via create_parser,
       if stdout is True print the result"""
    parser = create_parser()

    if args is None:
        args = parser.parse_args()

    ### Debug:
    # print(args)
    # raise SystemExit

    # taking the first operation in args namespace
    # if combo, e.g. -a and -s, take the first one
    for operation, numbers in vars(args).items():
        if numbers is None:
            continue

        try:
            res = calculator(operation, numbers)
        except ZeroDivisionError:
            res = 0

        if stdout:
            print(res)

        return res

    return None


if __name__ == '__main__':
    call_calculator(stdout=True)
