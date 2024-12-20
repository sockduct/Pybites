#! /usr/bin/env python3.13


from io import StringIO, TextIOWrapper
import json
from pathlib import Path
import re
from typing import Any
from urllib.request import urlretrieve


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'omdb_data'
URL = 'https://bites-data.s3.us-east-2.amazonaws.com'


# Types
File = str | Path | TextIOWrapper | StringIO
Movies = list[dict[str, Any]]

### To do - define dict with types for everything...

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


def get_movie_data(files: list[File]) -> list[dict[str, Any]]:
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


def get_single_comedy(movies: Movies) -> str:
    """
    return the movie with Comedy in Genres
    * Title key = movie name
    * Genre key = list of genres
    """

    # No error handling!!!
    return [movie['Title'] for movie in movies if 'Comedy' in movie['Genre']][0]


def get_movie_field(movies: Movies, field: str) -> dict[str, dict[str, str]]:
    return {movie['Title']: {field.lower(): movie[field]} for movie in movies}


def get_movie_most_nominations(movies: Movies) -> str:
    """
    Return the movie that had the most nominations

    Data Format:
    * "Awards": "Nominated for 1 Oscar. Another 10 wins & 32 nominations.",
    """
    data = get_movie_field(movies, 'Awards')

    for movie, movie_data in data.items():
        movie_total = 0
        if nom1 := re.search(r'nominated for (\d+) oscars?', movie_data['awards'], re.IGNORECASE):
            movie_total += int(nom1[1])
        if (nom2 := re.search(r'(\d+) wins? & (\d+) nominations?', movie_data['awards'],
                              re.IGNORECASE)
        ):
            movie_total += int(nom2[2])

        data[movie]['nominations'] = movie_total

    return sorted(
        ((movie, movie_data['nominations']) for movie, movie_data in data.items()),
        key=lambda e: e[1]
    )[-1][0]


def get_movie_longest_runtime(movies: Movies) -> str:
    """
    Return the movie that has the longest runtime

    Data Format:
    * "Runtime": "98 min",
    """
    data = get_movie_field(movies, 'Runtime')

    for movie, movie_data in data.items():
        if not (res := re.search(r'(\d+) min', movie_data['runtime'], re.IGNORECASE)):
            raise ValueError('Expected ## min, got:  movie_data["runtime"]')

        data[movie]['mins'] = int(res[1])

    return sorted(
        ((movie, movie_data['mins']) for movie, movie_data in data.items()),
        key=lambda e: e[1]
    )[-1][0]


if __name__ == '__main__':
    get_data(filext='.json')

    files: list[File] = []
    with open(f'{DATADIR/DATAFILE}.json', encoding='utf8') as infile:
        files.extend(StringIO(json_data_line) for json_data_line in infile)

    movie_data = get_movie_data(files)
    comedy = get_single_comedy(movie_data)
    most_nominations = get_movie_most_nominations(movie_data)
    longest = get_movie_longest_runtime(movie_data)
