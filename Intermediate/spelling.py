#! /usr/bin/env python3.13
'''
In this Bite you will write a simple spelling corrector. Complete suggest_word
that receives a misspelled word argument and returns the best matching
alternative word based on similarity ratio.

We recommend using difflib.SequenceMatcher in combination with the provided word
dictionary (loaded into words in the function).

Here are some example fixes for some common spelling mistakes:
>>> from spelling import suggest_word
>>> for misspelled_word in 'prfomnc abberration acommodation definately'.split():
...     print(misspelled_word, ' -> ', suggest_word(misspelled_word))
...
prfomnc  ->  'performance'
abberration  ->  'aberration'
acommodation  ->  'accommodation'
definately  ->  'definitely'

Pretty cool, no? Have fun, and keep calm and code in Python!
'''


from difflib import SequenceMatcher, get_close_matches
from functools import cache
import os
from pathlib import Path
import sys
from urllib.request import urlretrieve

sys.path.append(str(Path(__file__).resolve().parent.parent))
from basetmpl import get_data, get_path


TMP = os.getenv("TMP", "/tmp")
'''
DICTIONARY = os.path.join(TMP, 'dictionary.txt')
if not os.path.isfile(DICTIONARY):
    urlretrieve(
        'https://bites-data.s3.us-east-2.amazonaws.com/dictionary.txt',
        DICTIONARY
    )
'''
#
CWD = Path(__file__).parent
# Where to store retrieved data:
DATADIR = CWD/'data'
# Filename for retrieved data:
DATAFILE = 'dictionary.txt'
DICTIONARY = DATADIR/DATAFILE


@cache
def load_words(dictionary: str|Path=DICTIONARY) -> set[str]:
    'return dict of words in DICTIONARY'
    with open(dictionary) as f:
        return {word.strip().lower() for word in f.readlines()}


def suggest_word(misspelled_word: str, words: set[str]|None=None) -> str:
    """Return a valid alternative word that best matches
       the entered misspelled word"""
    if words is None:
        words = load_words()

    return get_close_matches(misspelled_word, words, n=1)[0]


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=False)

    for bad, expected in (
        ('prfomnc', 'performance'), ('abberration', 'aberration'),
        ('acommodation', 'accommodation'), ('definately', 'definitely'),
    ):
        print(f'{bad} => {suggest_word(bad)}, Expected {expected}')
