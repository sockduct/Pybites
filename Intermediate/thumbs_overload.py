#! /usr/bin/env python3.13
'''
In this Bite we learn a bit of operator overloading. Finish the Thumbs class
that returns an amount of thumbs up (👍) or thumbs down (👎) emojis based on
the int it is multiplied with.

Override the corresponding dunder methods to make this work. No constructor
method should be needed, the thumbs emojis to be used are defined in constants.

Best to see it in action using the REPL:
>>> from thumbs import Thumbs
>>> th = Thumbs()
>>> th * 1
'👍'
>>> th * 2
'👍👍'
>>> th * 3
'👍👍👍'

Starting 4 it shortens by returns the emoji once, followed by the amount in
parentheses:
>>> th * 4
'👍 (4x)'
>>> th * 5
'👍 (5x)'
>>> th * 6
'👍 (6x)'
...

For negative numbers the emoji changes from thumbs up to thumbs down:
>>> th * -1
'👎'
>>> th * -2
'👎👎'
>>> th * -3
'👎👎👎'

Again starting 4 it shows the number in parentheses (this was a real world use
case actually):
>>> th * -4
'👎 (4x)'
>>> th * -5
'👎 (5x)'
>>> th * -6
'👎 (6x)'
...

It should raise an exception if the number is 0:
>>> th * 0
Traceback (most recent call last):
...
ValueError: Specify a number

And lastly it should work both ways:
>>> th * 1
'👍'
>>> 1 * th
'👍'
>>> -3 * th
'👎👎👎'
>>> 7 * th
'👍 (7x)'
>>> -6 * th
'👎 (6x)'
>>> 0 * th
...
ValueError: Specify a number

We hope this shows you a bit of the power of operator overloading. If you want
to learn more about Python's data model and dunder methods, check out Bob's
guest post: Enriching Your Python Classes With Dunder (Magic, Special) Methods
(https://dbader.org/blog/python-dunder-methods).
'''


from typing import Self


THUMBS_UP, THUMBS_DOWN = '👍', '👎'


class Thumbs:
    def __mul__(self, other: int) -> str:
        '''
        Alternate implementation:
        emoji = THUMBS_UP if count > 0 else THUMBS_DOWN
        count = abs(count)

        if count == 0:
            raise ValueError('Specify a number')

        return f'{emoji} ({count}x)' if count > 3 else emoji * count
        '''
        match other:
            case 0:
                raise ValueError('Specify a number')
            case n if 4 > n > 0:
                return THUMBS_UP * n
            case n if n >= 4:
                return f'{THUMBS_UP} ({n}x)'
            case n if -4 < n < 0:
                return THUMBS_DOWN * abs(n)
            case n if n <= -4:
                return f'{THUMBS_DOWN} ({abs(n)}x)'
            case _:
                return NotImplemented

    def __rmul__(self, other: int) -> str:
        return self * other


if __name__ == '__main__':
    values = list(range(-6, 7))
    # Incorrect type on purpose for testing:
    values.append('bad')  # type: ignore
    thumb = Thumbs()
    for value in values:
        try:
            print(f'Forward:  thumb * {value} => {thumb * value}')
        except Exception as err:
            print(f'Forward:  thumb * {value} raised:\n{err}')

        try:
            print(f'Reverse:  {value} * thumb => {value * thumb}')
        except Exception as err:
            print(f'Reverse:  {value} * thumb raised:\n{err}')
