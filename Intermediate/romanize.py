#! /usr/bin/env python3.13
'''
Complete romanize that takes a decimal number and converts it to its Roman
Numeral equivalent.

If a non int or invalid number (<= 0 or >= 4000) is given raise a ValueError.
'''


def romanize(decimal_number: int) -> str:
    """Takes a decimal number int and converts its Roman Numeral str"""
    d2r = {1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L',
           90: 'XC', 100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1_000: 'M'}
    res = []

    if not (dec := isinstance(decimal_number, int)) or not 0 < decimal_number < 4_000:
        if dec:
            err_msg = f'{decimal_number:,} is out of range.'
        else:
            err_msg = f'{decimal_number} is not an integer.'
        raise ValueError(f'Must be an integer between 1 - 3,999.  {err_msg}')

    '''
    Algorithm:
    * Look for highest key >= decimal_number and append to result
    * If create sequence of more than 3 - error!

    Alternate approach:
    # Could reverse order of dict too so didn't have to use reversed...
    for number, numeral in reversed(d2r.items()):
    while decimal_number >= number:
        result += numeral
        decimal_number -= number
    '''
    current = decimal_number
    while current > 0:
        digit = max(key for key in d2r if key <= current)
        res.append(d2r[digit])
        current -= digit

    return ''.join(res)


if __name__ == '__main__':
    try:
        print(romanize(0))
    except ValueError as err:
        print(err)
    print(romanize(1))
    print(romanize(1839))
    print(romanize(3999))
    try:
        print(romanize(4000))
    except ValueError as err:
        print(err)
    try:
        # Purposely providing illegal value to test error handling:
        print(romanize(5.4))  # type: ignore
    except ValueError as err:
        print(err)
    try:
        # Purposely providing illegal value to test error handling:
        print(romanize('string'))  # type: ignore
    except ValueError as err:
        print(err)
