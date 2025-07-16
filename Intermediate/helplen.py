#! /usr/bin/env python3.13
'''
Sometimes you need to capture stdout in your script. Python makes it easy with
contextlib's redirect_stdout.

In this Bite you will use it to get the length of a help text as returned by
help.

Complete get_len_help_text which receives a builtin. Run help against this
builtin and capture its output in a variable and return its length (number of
chars). If a non-builtin is passed into the function, raise a ValueError (hint:
you can use BuiltinFunctionType to check this).

Here you see the function in action:
>>> from helplen import get_len_help_text
>>> get_len_help_text(max)
402
>>> get_len_help_text(pow)
278
>>> get_len_help_text('bogus')
...
ValueError
'''


from contextlib import redirect_stdout
from io import StringIO
from types import BuiltinFunctionType


def get_len_help_text(builtin: BuiltinFunctionType) -> int:
    """Receives a builtin, and returns the length of its help text.
       You need to redirect stdout from the help builtin.
       If the the object passed in is not a builtin, raise a ValueError.
    """
    if not isinstance(builtin, BuiltinFunctionType):
        raise ValueError(
            f'Expected builtin to be of type BuiltinFunctionType, got {builtin.__class__.__name__}'
        )
    with redirect_stdout(StringIO()) as output:
        help(builtin)

    return len(output.getvalue())


if __name__ == '__main__':
    try:
        # For Python 3.13 on Windows x64:
        for builtin, length in ((max, 409), (pow, 278), ('bogus', 'ValueError')):
            # Purposefully sending invalid type to test exception handling:
            print(f'{get_len_help_text(builtin)=}, expected {length}')  # type: ignore
    except TypeError:
        print(f'get_len_help_text({builtin}) => ValueError, expected {length}')
