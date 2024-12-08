#! /usr/bin/env python3.13


from difflib import SequenceMatcher
from itertools import combinations
import os
from pathlib import Path
import re
from urllib.request import urlretrieve


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'tags.xml'
DATA = CWD/DATADIR/DATAFILE
#
# Included:
TAG_HTML = re.compile(r'<category>([^<]+)</category>')
TMP = os.getenv("TMP", "/tmp")
TEMPFILE = os.path.join(TMP, 'feed')
MIN_TAG_LEN = 10
IDENTICAL = 1.0
SIMILAR = 0.95


# Types
file = Path | str

# Module
def get_data(verbose: bool=False) -> None:
    if not DATADIR.exists():
        DATADIR.mkdir()

    if not DATA.exists():
        if verbose:
            print(f'Retrieving data and saving to {DATA}.')
        # Retrieve DATA:
        urlretrieve(
            'https://bites-data.s3.us-east-2.amazonaws.com/tags.xml',
            DATA
        )
    elif verbose:
        print(f'{DATA} already present.')


def _get_tags(tempfile: file=TEMPFILE) -> set[str]:
    """Helper to parse all tags from a static copy of PyBites' feed,
       providing this here so you can focus on difflib"""
    with open(tempfile) as f:
        content = f.read().lower()
    # take a small subset to keep it performant
    tags = TAG_HTML.findall(content)
    tags = [tag for tag in tags if len(tag) > MIN_TAG_LEN]
    return set(tags)


def get_similarities(tags: set[str]|None=None) -> list[tuple[str, str]]:
    """Should return a list of similar tag pairs (tuples)"""
    file = DATA if 'DATA' in globals() else TEMPFILE
    tags = tags or _get_tags(file)
    '''
    # Original solution:
    matches = []

    # do your thing ...
    for tag1, tag2 in combinations(tags, 2):
        ratio = SequenceMatcher(None, tag1, tag2).ratio()
        if ratio > SIMILAR:
            matches.append((tag1, tag2))
            if verbose:
                print(f'Hit:  {tag1} is {(100 * ratio):.2f}% simlar to {tag2}')
    '''

    # Improved solution based on looking at forum:
    return [
        pair for pair in combinations(tags, 2)
        if SequenceMatcher(None, *pair).ratio() > SIMILAR
    ]


if __name__ == '__main__':
    get_data(verbose=True)
    print(get_similarities())
