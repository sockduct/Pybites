#! /usr/bin/env python3

"""A palindrome is a word, phrase, number, or other sequence of characters
which reads the same backward as forward"""


from pathlib import Path
# Generators (functions/expressions) typically use Iterator type:
from typing import Iterable, Iterator
import urllib.request


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'dictionary_m_words.txt'
DATA = DATADIR/DATAFILE


# Module
def get_data() -> None:
    if not DATADIR.exists():
        DATADIR.mkdir()

    if not DATA.exists():
        print(f'Retrieving data and saving to {DATA}.')
        # Retrieve DATA:
        urllib.request.urlretrieve(
            'https://bites-data.s3.us-east-2.amazonaws.com/dictionary_m_words.txt',
            DATA
        )
    else:
        print(f'{DATA} already present.')


def load_dictionary(dictionary: Path=DATA) -> Iterator[str]:
    """Load dictionary (sample) and return as generator (done)"""
    with open(dictionary) as f:
        return (word.lower().strip() for word in f.readlines())


def is_palindrome(word: str) -> bool:
    """Return if word is palindrome, 'madam' would be one.
       Case insensitive, so Madam is valid too.
       It should work for phrases too so strip all but alphanumeric chars.
       So "No 'x' in 'Nixon'" should pass (see tests for more)"""
    '''
    Alternatively:
    word = re.sub(r'\W+', '', word.lower())
    '''
    word_alt = ''.join(char.lower() for char in word if char.isalnum())
    return word_alt == word_alt[::-1]


def get_longest_palindrome(words: Iterable[str]|None=None) -> str:
    """Given a list of words return the longest palindrome
       If called without argument use the load_dictionary helper
       to populate the words list"""
    if words is None:
        words = load_dictionary()

    return max((word for word in words if is_palindrome(word)), key=len)


if __name__ == '__main__':
    get_data()
    dict_words = load_dictionary()
    print(f'Longest palindrome from {DATA}:\n{get_longest_palindrome(dict_words)}')

    new_longest = 'A car, a man, a maraca.'
    words = list(dict_words) + [new_longest]
    print(f'New longest palindrome:\n{get_longest_palindrome(words)}')
