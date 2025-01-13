#! /usr/bin/env python3.13


import argparse


def calculator(operation, numbers):
    """TODO 1:
       Create a calculator that takes an operation and list of numbers.
       Perform the operation returning the result rounded to 2 decimals"""
    pass


def create_parser() -> argparse.ArgumentParser:
    """TODO 2:
       Create an ArgumentParser object:
       - have one operation argument,
       - have one or more integers that can be operated on.
       Returns a argparse.ArgumentParser object.

       Note that type=float times out here so do the casting in the calculator
       function above!"""
    parser = argparse.ArgumentParser(
        # prog='Simple Calculator',
        description='Add/Subtract/Multiple/Divide a list of numbers'
    )
    parser.add_argument(
        '-a', '--add', action='extend', nargs='+', type=float, metavar='num',
        help='Add a list of numbers'
    )
    parser.add_argument(
        '-s', '--sub', action='extend', nargs='+', type=int, metavar='num',
        help='Subtract a list of numbers'
    )
    parser.add_argument(
        '-d', '--div', action='extend', nargs='+', type=int, metavar='num',
        help='Divide a list of numbers'
    )
    parser.add_argument(
        '-m', '--mul', action='extend', nargs='+', type=int, metavar='num',
        help='Multiply a list of numbers'
    )

    return parser


def call_calculator(args=None, stdout=False):
    """Provided/done:
       Calls calculator with provided args object.
       If args are not provided get them via create_parser,
       if stdout is True print the result"""
    parser = create_parser()

    if args is None:
        args = parser.parse_args()

    ### Debug:
    print(args)
    raise SystemExit

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


if __name__ == '__main__':
    call_calculator(stdout=True)
