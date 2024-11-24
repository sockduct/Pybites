#! /usr/bin/env python3


number = int | float

# Module
def positive_divide(numerator: number, denominator: number) -> number:
    try:
        res = numerator/denominator
    except ZeroDivisionError:
        return 0
    except (TypeError, ValueError):
        raise
    else:
        if res < 0:
            raise ValueError('Can\'t be negative!')

        return res
