#! /usr/bin/env python3.13
'''
Implement the Color class:
* add self.rgb to the __init__ method that gets its value from the provided
  COLOR_NAMES dictionary (k, v = color_name, rgb-tuple;
  e.g.: "ALICEBLUE": (240, 248, 255))
* If the value does not exist, assume it is None.
* Convert hex2rgb and rgb2hex into @staticmethods.
* Validate the values being passed to each of these staticmethods and raise a
  ValueError if called with bad data.
* Add a __repr__ method whose value is in the form of Color('white'), with white
  being the value that it was initialized with.
* Add a __str__ method whose value is the RGB value of the color if it is found
  in COLOR_NAMES, else return Unknown.
* Take a look at the tests for a better understanding of the values expected.
'''

from contextlib import suppress
from pathlib import Path
import re
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from basetmpl import get_data, get_path

CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'color_values.py'

sys.path.append(str(Path(DATADIR)))
try:
    from color_values import COLOR_NAMES  # type: ignore
except ImportError:
    print(
        'Warning:  Unable to import color_values - try again after running this as the main module.'
    )


class Color:
    """
    Color class.

    Takes the string of a color name and returns its RGB value.
    """

    def __init__(self, color: str):
        self._color = color
        self.rgb = COLOR_NAMES.get(color.upper())

    @staticmethod
    def hex2rgb(hex: str) -> tuple[int, ...]:
        """Class method that converts a hex value into an rgb one"""
        '''
        # Overkill!!!
        errmsg = 'Expected string of form #[0-9a-f]x6, e.g., "#00ff7e", not "{}".'
        if not isinstance(hex, str) or not re.match(
            r'#[0-9a-fx]{6,12}$', (hex_val := hex.strip().lower())
        ):
            raise ValueError(errmsg.format(hex))

        hex_stack = list(hex_val)
        current = []
        hex_res = []
        while hex_stack:
            current.insert(0, hex_stack.pop())
            match current:
                case ['#']:
                    break
                case [d1] | ['x', d1]:
                    continue
                case ['0', 'x', d1]:
                    hex_res.insert(0, f'0{d1}')
                    current = []
                case [d1, d2] | ['x', d1, d2]:
                    continue
                case ['#', d1, d2]:
                    hex_res.insert(0, d1 + d2)
                    current = []
                case [d1, d2, d3]:
                    hex_res.insert(0, d2 + d3)
                    current = [d1]
                case ['0', 'x', d1, d2]:
                    hex_res.insert(0, d1 + d2)
                    current = []
                case _:
                    raise ValueError(errmsg.format(hex))

        hex_num = ''.join(hex_res)
        return tuple(int(hex_num[i:i + 2], base=16) for i in (0, 2, 4))
        '''
        if not isinstance(hex, str) or not re.match(r'#[0-9a-f]{6}$', (hex_val := hex.strip().lower())):
            raise ValueError(
                f'Expected string of form #[0-9a-f]x6, e.g., "#00ff7e", not "{hex}".'
            )

        return tuple(int(hex_val[i:i + 2], base=16) for i in (1, 3, 5))


    @staticmethod
    def rgb2hex(rgb: list[int]|tuple[int, int, int]) -> str:
        """Class method that converts an rgb value into a hex one"""
        if not isinstance(rgb, (list, tuple)) or not all(isinstance(val, int) for val in rgb) or (
            not all(0 <= num <= 255 for num in rgb) or len(rgb) != 3
        ):
            raise ValueError(
                f'Expected tuple of 3 integers from 0 - 255, e.g., (0, 127, 255), not "{rgb}".'
            )

        return f"#{''.join(f'{num:02x}' for num in rgb)}"

    def __repr__(self) -> str:
        """Returns the repl of the object"""
        return f"Color('{self._color}')"

    def __str__(self) -> str:
        """Returns the string value of the color object"""
        return f'{self.rgb}' if self.rgb is not None else 'Unknown'


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=True)

    if 'COLOR_NAMES' not in globals():
        from color_values import COLOR_NAMES

    Color('white')
    Color('bad')
    with suppress(ValueError):
        Color.hex2rgb('bad')
    Color.hex2rgb('#ff00e7')
    Color.hex2rgb('#0xff0x000xe7')

    # Ignore types when intentionally sending invalid values for testing:
    with suppress(ValueError):
        Color.hex2rgb(1227)  # type: ignore
    with suppress(ValueError):
        Color.rgb2hex('abc')  # type: ignore
    with suppress(ValueError):
        Color.rgb2hex(122345)  # type: ignore
    with suppress(ValueError):
        Color.rgb2hex(['a'])  # type: ignore
    with suppress(ValueError):
        Color.rgb2hex([1, 2])

    Color.rgb2hex([11, 22, 33])
    print(repr(Color('black')))
    print(Color('white'))
