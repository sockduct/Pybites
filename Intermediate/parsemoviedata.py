#! /usr/bin/env python3.13


from functools import singledispatch
from io import StringIO, TextIOWrapper
import json
from pathlib import Path
import re
from typing import Literal, TypedDict
from urllib.request import urlretrieve


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'omdb_data'
URL = 'https://bites-data.s3.us-east-2.amazonaws.com'


# Types
File = str | Path | TextIOWrapper | StringIO

class Movie(TypedDict):
    Title: str
    Year: str
    Rated: str
    Released: str
    Runtime: str
    Genre: str
    Director: str
    Writer: str
    Actors: str
    Plot: str
    Language: str
    Country: str
    Awards: str
    Poster: str
    Ratings: list[dict[str, str]]
    Metascore: str
    imdbRating: str
    imdbVotes: str
    imdbID: str
    Type: str
    DVD: str
    BoxOffice: str
    Production: str
    Website: str
    Response: str


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


@singledispatch
def load_json_data(json_file: object) -> Movie:
    raise NotImplementedError


@load_json_data.register
def _(json_file: str|Path) -> Movie:
    with open(json_file, encoding='utf8') as infile:
        data: Movie = json.load(infile)
    return data


@load_json_data.register
def _(json_file: TextIOWrapper|StringIO) -> Movie:
    data: Movie = json.load(json_file)
    return data


def get_movie_data(files: list[File]) -> list[Movie]:
    """Parse movie json files into a list of dicts"""
    return [load_json_data(json_file) for json_file in files]


# Ideally would include all possible Movie fields in Literal list:
def get_movie_field(movies: list[Movie], field: Literal['Awards', 'Genre', 'Runtime']
                    ) -> dict[str, str|list[dict[str, str]]]:
    return {movie['Title']: movie[field] for movie in movies}


def get_single_comedy(movies: list[Movie]) -> str|None:
    """
    return the movie with Comedy in Genres
    * Title key = movie name
    * Genre key = list of genres
    """
    data = get_movie_field(movies, 'Genre')
    comedies = [movie for movie, genre in data.items() if 'Comedy' in genre]
    return comedies[0] if comedies else None


def get_nominations(awards: str) -> int:
    movie_total = 0
    if nom1 := re.search(r'nominated for (\d+) oscars?', awards, re.IGNORECASE):
        movie_total += int(nom1[1])
    if nom2 := re.search(r'(\d+) wins? & (\d+) nominations?', awards, re.IGNORECASE):
        movie_total += int(nom2[2])
    return movie_total


def get_movie_most_nominations(movies: list[Movie]) -> str:
    """
    Return the movie that had the most nominations

    Data Format:
    * "Awards": "Nominated for 1 Oscar. Another 10 wins & 32 nominations.",
    """
    data = get_movie_field(movies, 'Awards')

    # Need to ignore typing as mypy complains awards could be str|list[dict[str,str]] from Movie
    # TypedDict definition - apparently doesn't understand this particular key is only a str...
    nominations = {movie: get_nominations(awards) for movie, awards in data.items()} # type: ignore
    return max(nominations, key=lambda e: nominations[e])


def get_runtime(runtime: str) -> int:
    return int(res[1]) if (res := re.search(r'(\d+) min', runtime, re.IGNORECASE)) else 0


def get_movie_longest_runtime(movies: list[Movie]) -> str:
    """
    Return the movie that has the longest runtime

    Data Format:
    * "Runtime": "98 min",
    """
    data = get_movie_field(movies, 'Runtime')

    # Need to ignore typing as mypy complains awards could be str|list[dict[str,str]] from Movie
    # TypedDict definition - apparently doesn't understand this particular key is only a str...
    runtime = {movie: get_runtime(runtime) for movie, runtime in data.items()} # type: ignore
    return max(runtime, key=lambda e: runtime[e])


if __name__ == '__main__':
    get_data(filext='.json')

    files: list[File] = []
    with open(f'{DATADIR/DATAFILE}.json', encoding='utf8') as infile:
        files.extend(StringIO(json_data_line) for json_data_line in infile)

    movie_data = get_movie_data(files)
    comedy = get_single_comedy(movie_data)
    most_nominations = get_movie_most_nominations(movie_data)
    longest = get_movie_longest_runtime(movie_data)
