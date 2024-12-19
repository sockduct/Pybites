#! /usr/bin/env python3.13


from io import StringIO, TextIOWrapper
import json
from pathlib import Path
from typing import Any
from urllib.request import urlretrieve


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'omdb_data'
URL = 'https://bites-data.s3.us-east-2.amazonaws.com'


# Types
file = str|Path|TextIOWrapper|StringIO


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


def get_movie_data(files: list[file]) -> list[dict[str, Any]]:
    """Parse movie json files into a list of dicts"""
    movie_data = []
    for json_file in files:
        # file/path:
        try:
            with open(json_file, encoding='utf8') as infile:
                movie_data.append(json.load(infile))
        # In-memory buffer:
        except TypeError:
            movie_data.append(json.load(json_file))

    return movie_data


def get_single_comedy(movies: list[dict[str, Any]]) -> str:
    """
    return the movie with Comedy in Genres
    * Title key = movie name
    * Genre key = list of genres
    """

    # No error handling!!!
    return [movie['Title'] for movie in movies if 'Comedy' in movie['Genre']][0]


def get_movie_most_nominations(movies: list) -> str:
    """Return the movie that had the most nominations"""
    pass


def get_movie_longest_runtime(movies: list) -> str:
    """Return the movie that has the longest runtime"""
    pass


if __name__ == '__main__':
    get_data(filext='.json')

    files = []
    with open(f'{DATADIR/DATAFILE}.json', encoding='utf8') as infile:
        files.extend(StringIO(json_data_line) for json_data_line in infile)

    movie_data = get_movie_data(files)
    comedy = get_single_comedy(movie_data)
    ...
