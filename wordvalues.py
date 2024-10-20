import os
from pathlib import Path
import tempfile
import urllib.request

# PREWORK/CONSTANTS:
TMPDIR = tempfile.TemporaryDirectory()
# TMP = os.getenv("TMP", "/tmp")
TMP = os.getenv('TMP', TMPDIR)

CWD = Path(__file__).parent
S3 = 'https://bites-data.s3.us-east-2.amazonaws.com/'
DICT = 'dictionary.txt'

scrabble_scores = [(1, "E A O I N R T L S U"), (2, "D G"), (3, "B C M P"),
                   (4, "F H V W Y"), (5, "K"), (8, "J X"), (10, "Q Z")]
LETTER_SCORES = {letter: score for score, letters in scrabble_scores
                 for letter in letters.split()}

# start coding

def get_dict():
    # DICTIONARY = os.path.join(TMP, DICT)
    # dictionary = Path(TMP)/DICT
    dictionary_dir = CWD/'data'
    dictionary_file = dictionary_dir/DICT

    if not dictionary_dir.exists():
        dictionary_dir.mkdir()

    if not dictionary_file.exists():
        print(f'Retrieving dictionary and saving to {dictionary_file}.')
        urllib.request.urlretrieve(f'{S3}{DICT}', dictionary_file)
    else:
        print(f'{dictionary_file} already present.')

def load_words():
    """Load the words dictionary (DICTIONARY constant) into a list and return it"""
    pass


def calc_word_value(word):
    """Given a word calculate its value using the LETTER_SCORES dict"""
    pass


def max_word_value(words):
    """Given a list of words calculate the word with the maximum value and return it"""
    pass

if __name__ == '__main__':
    get_dict()
