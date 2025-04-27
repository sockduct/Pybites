#! /usr/bin/env python3.13
'''
In this Bite you are tasked with "physically" aligning the number of comments on
a webpage.

For some reason you are not allowed to use the pre tag so you are asked to
prepend each number with one or more HTML spaces (&nbsp;).

You need to make sure the comment counts line up vertically, so in order for the
web page to show this:
   1
  20
 315
1239

You need to produce this output:
&nbsp;&nbsp;&nbsp;1
&nbsp;&nbsp;20
&nbsp;315
1239

Complete prefill_with_character(value, column_length=4, fill_char=' ') to
achieve this.

Your code is expected to also work if other values are provided for the
column_length and fill_char arguments. Have fun!
'''


HTML_SPACE = '&nbsp;'


def prefill_with_character(value: int, column_length: int=4, fill_char: str=HTML_SPACE) -> str:
    """Prepend value with fill_char for given column_length"""
    # return f'{fill_char * (column_length - len(str(value)))}{value}'
    # Better:
    return str(value).rjust(column_length, ' ').replace(' ', fill_char)


if __name__ == '__main__':
    for test_val in (1, 20, 315, 1239):
        print(prefill_with_character(test_val))
