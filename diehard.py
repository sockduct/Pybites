#! /usr/bin/env python3


from collections import Counter, namedtuple
from pathlib import Path
from typing import NamedTuple, Iterator
import urllib.request


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'dirnames.txt'
DATA = CWD/DATADIR/DATAFILE


IGNORE = ['static', 'templates', 'data', 'pybites', 'bbelderbos', 'hobojoe1848']
class Stats(NamedTuple):
    user: str
    challenge: str


# Module
def get_data() -> None:
    if not DATADIR.exists():
        DATADIR.mkdir()

    if not DATA.exists():
        print(f'Retrieving data and saving to {DATA}.')
        # Retrieve DATA:
        urllib.request.urlretrieve(
            'https://bites-data.s3.us-east-2.amazonaws.com/dirnames.txt',
            DATA
        )
    else:
        print(f'{DATA} already present.')


def gen_files(tempfile: Path=DATA) -> Iterator[str]:
    """
    Parse the tempfile passed in, filtering out directory names
    (first column) using the last "is_dir" column.

    Lowercase these directory names and return them as a generator.

    "tempfile" has the following format:
    challenge<int>/file_or_dir<str>,is_dir<bool>

    For example:
    03/rss.xml,False
    03/tags.html,False
    03/Mridubhatnagar,True
    03/aleksandarknezevic,True

    => Here you would return 03/mridubhatnagar (lowercased!)
       followed by 03/aleksandarknezevic
    """
    booldict = {'True': True, 'False': False}

    with open(tempfile) as infile:
        for line in infile:
            data, flag = line.strip().split(',')
            if flag := booldict[flag.title()]:
                yield data.lower()


def diehard_pybites(files: list[str]|None=None):
    """
    Return a Stats namedtuple (defined above) that contains:
    1. the user that made the most pull requests (ignoring the users in IGNORE), and
    2. a tuple of:
        ("most popular challenge id", "amount of pull requests for that challenge")

    Calling this function on the default dirnames.txt should return:

    Stats(user='clamytoe', challenge=('01', 7))
    """
    if files is None:
        files = gen_files()

    ucstats = [Stats((res := item.split('/')).reverse()) for item in files]
    users = Counter(user.user for user in ucstats)
    popular_challenges = Counter(challenge.challenge for challenge in ucstats)

    print(f'{users=}, {popular_challenges=}')


if __name__ == '__main__':
    get_data()
    # print(list(gen_files()))
    diehard_pybites()
