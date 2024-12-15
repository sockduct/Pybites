#! /usr/bin/env python3.13


from collections import Counter
import os
from pathlib import Path
import string
import urllib.request


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILES = ('stopwords.txt', 'harry.txt')
DATA = None
URL = 'https://bites-data.s3.us-east-2.amazonaws.com'

# data provided
tmp = os.getenv("TMP", "/tmp")
stopwords_file = os.path.join(tmp, 'stopwords')
harry_text = os.path.join(tmp, 'harry')
'''
urllib.request.urlretrieve(
    'https://bites-data.s3.us-east-2.amazonaws.com/stopwords.txt',
    stopwords_file
)
urllib.request.urlretrieve(
    'https://bites-data.s3.us-east-2.amazonaws.com/harry.txt',
    harry_text
)
'''


# Module
def get_data(datafile: str|None=DATA, datadir: Path=DATADIR, url: str=URL) -> None:
    if not datafile:
        raise FileNotFoundError('Please pass in a file to retrieve.')

    if not datadir.exists():
        datadir.mkdir()

    data = datadir/datafile
    if not data.exists():
        print(f'Retrieving data and saving to {data}.')
        # Retrieve data:
        urllib.request.urlretrieve(f'{url}/{datafile}', data)
    else:
        print(f'{data} already present.')


def get_words(file: str|Path) -> list[str]:
    if hasattr(file, 'read_text'):
        return list(file.read_text(encoding='utf8').split())

    with open(file, encoding='utf8') as infile:
        return list(infile.read().split())


def process_words(stop_words: list[str], harry: list[str]) -> list[str]:
    # Approach one - strip out non-alphanumeric characters:
    nonalphanum = string.punctuation + string.whitespace

    '''
    # Too convoluted and three calls to word_fix = no!
    word_fix = lambda word: word.lower().strip(nonalphanum)
    ac = [word_fix(word) for word in harry if word_fix(word) and word_fix(word) not in stop_words]
    '''
    candidates = []
    for word in harry:
        word = word.lower().strip(nonalphanum)
        if word and word not in stop_words:
            candidates.append(word)

    return candidates


def get_harry_most_common_word() -> tuple[str, int]:
    # file = DATA if 'DATA' in globals() else TEMPFILE
    stop_words_file = DATADIR/DATAFILES[0] if 'DATADIR' in globals() else stopwords_file
    harry_file = DATADIR/DATAFILES[1] if 'DATADIR' in globals() else harry_text

    # Get list of words from files:
    stop_words = get_words(stop_words_file)
    harry = get_words(harry_file)

    # Process words:
    candidates = process_words(stop_words, harry)

    return Counter(candidates).most_common(1)[0]


if __name__ == '__main__':
    for datafile in DATAFILES:
        get_data(datafile)

    print(get_harry_most_common_word())
