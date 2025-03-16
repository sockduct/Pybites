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

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from basetmpl import get_data, get_path


CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'color_values.py'


class Color:
    """
    Color class.

    Takes the string of a color name and returns its RGB value.
    """

    def __init__(self, color: str):
        self.rgb = COLOR_NAMES[color.upper()]

    @classmethod
    def hex2rgb(cls):
        """Class method that converts a hex value into an rgb one"""
        pass

    @classmethod
    def rgb2hex(cls):
        """Class method that converts an rgb value into a hex one"""
        pass

    def __repr__(self):
        """Returns the repl of the object"""
        pass

    def __str__(self):
        """Returns the string value of the color object"""
        pass


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=False)

    sys.path.append(str(Path(DATADIR)))
    from color_values import COLOR_NAMES
