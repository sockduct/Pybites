#! /usr/bin/env python3.13
'''
In this Bite you complete a function that takes an int and returns it appended
with the right suffix: 1 -> 1st, 2 -> 2nd, 4 -> 4th, 11 -> 11th, etc.

As per Wikipedia the rules are:
* -st is used with numbers ending in 1 (e.g. 1st, pronounced first)
* -nd is used with numbers ending in 2 (e.g. 92nd, pronounced ninety-second)
* -rd is used with numbers ending in 3 (e.g. 33rd, pronounced thirty-third).
* An exception to the above rules, all the "teen" numbers ending with 11, 12 or
  13 use -th (e.g. 11th, pronounced eleventh, 112th, pronounced one hundred
  [and] twelfth)
* -th is used for all other numbers (e.g. 9th, pronounced ninth).

To focus on the exercise you can assume that the number inputted into the
function is a positive int. Good luck and keep calm and code in Python!
'''


def get_ordinal_suffix(number: int) -> str:
    """Receives a number int and returns it appended with its ordinal suffix,
       so 1 -> 1st, 2 -> 2nd, 4 -> 4th, 11 -> 11th, etc.

       Rules:
       https://en.wikipedia.org/wiki/Ordinal_indicator#English
       - st is used with numbers ending in 1 (e.g. 1st, pronounced first)
       - nd is used with numbers ending in 2 (e.g. 92nd, pronounced ninety-second)
       - rd is used with numbers ending in 3 (e.g. 33rd, pronounced thirty-third)
       - As an exception to the above rules, all the "teen" numbers ending with
         11, 12 or 13 use -th (e.g. 11th, pronounced eleventh, 112th,
         pronounced one hundred [and] twelfth)
       - th is used for all other numbers (e.g. 9th, pronounced ninth).
       """
    '''
    Alternative solution:
    number = str(number)
    first_three = dict(zip('1 2 3'.split(), 'st nd rd'.split()))
    suffix = first_three.get(number[-1]) or 'th'
    # 'teen' number override
    if len(number) > 1 and number[-2] == '1':
        suffix = 'th'
    return f'{number}{suffix}'
    '''
    match str(number):
        case n if n.endswith('11') or n.endswith('12') or n.endswith('13'):
            return f'{n}th'
        case n if n.endswith('1'):
            return f'{n}st'
        case n if n.endswith('2'):
            return f'{n}nd'
        case n if n.endswith('3'):
            return f'{n}rd'
        case _:
            return f'{n}th'


if __name__ == '__main__':
    for num in (1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 14, 17, 21, 32, 111):
        print(f'{num} => {get_ordinal_suffix(num)}')
