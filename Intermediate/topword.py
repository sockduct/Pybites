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

stopwords_file = os.path.join(tmp, 'stopwords')
harry_text = os.path.join(tmp, 'harry')

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


def get_harry_most_common_word(stop_words_file: str|Path=stopwords_file,
                               harry_file: str|Path=harry_text) -> tuple[str, int]:
    # file = DATA if 'DATA' in globals() else TEMPFILE

    stop_words = get_words(stop_words_file)
    harry = get_words(harry_file)

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

    return Counter(candidates).most_common(1)[0]


if __name__ == '__main__':
    for datafile in DATAFILES:
        get_data(datafile)

    datafiles = tuple(DATADIR/datafile for datafile in DATAFILES)
    print(get_harry_most_common_word(*datafiles))
