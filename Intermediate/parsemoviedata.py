#! /usr/bin/env python3.13


import json
from pathlib import Path
from urllib.request import urlretrieve


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'omdb_data'
URL = 'https://bites-data.s3.us-east-2.amazonaws.com'


# Module
### Updates ###
def get_data(datafile: str=DATAFILE, datadir: Path=DATADIR, url: str=URL,
             filext: str='.txt') -> None:
    if not datadir.exists():
        datadir.mkdir()

    if not (datafilep := Path(datafile)).suffix:
        datafilep = datafilep.with_suffix(filext)

    data = datadir/datafilep
    if not data.exists():
        print(f'Retrieving data and saving to {data}.')
        urlretrieve(f'{url}/{datafile}', data)
    else:
        print(f'{data} already present.')


def get_movie_data(files: list) -> list:
    """Parse movie json files into a list of dicts"""
    pass


def get_single_comedy(movies: list) -> str:
    """return the movie with Comedy in Genres"""
    pass


def get_movie_most_nominations(movies: list) -> str:
    """Return the movie that had the most nominations"""
    pass


def get_movie_longest_runtime(movies: list) -> str:
    """Return the movie that has the longest runtime"""
    pass


if __name__ == '__main__':
    get_data(filext='.json')
