#! /usr/bin/env python3.13
'''
Get all valid dictionary words for a random draw of 7 letters.
'''


from itertools import permutations
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from basetmpl import get_data, get_path


# Globals:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'dictionary.txt'
URL = 'https://bites-data.s3.us-east-2.amazonaws.com'


# def get_possible_dict_words(draw: list[str]) -> list[str]:
def get_possible_dict_words(draw: list[str]) -> set[str]:
    """Get all possible words from a draw (list of letters) which are
       valid dictionary words. Use _get_permutations_draw and provided
       dictionary"""
    '''
    Alternative:
    possible = _get_permutations_draw(draw)
    dictionary = _get_dictionary()
    return [option for option in possible if option in dictionary]
    '''
    return set(_get_permutations_draw(draw)) & _get_dictionary()


def _get_dictionary(datapath: str|Path=DATADIR/DATAFILE) -> set[str]:
    with open(datapath) as f:
        return {word.strip().lower() for word in f.read().split()}


def _get_permutations_draw(draw: list[str]) -> list[str]:
    """Helper to get all permutations of a draw (list of letters), hint:
       use itertools.permutations (order of letters matters)"""
    draw = [letter.lower() for letter in draw]
    return [''.join(permutation)
            for n in range(1, len(draw) + 1)
            for permutation in permutations(draw, r=n)]


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=True)

    res = get_possible_dict_words(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
