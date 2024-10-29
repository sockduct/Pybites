#! /usr/bin/env python3

import csv
from collections import defaultdict, namedtuple
import json
import os
from pathlib import Path
from pprint import pformat, pprint
from statistics import mean
from urllib.request import urlretrieve


# Global Constants:
CWD = Path(__file__).parent

BASE_URL = 'https://bites-data.s3.us-east-2.amazonaws.com/'
# TMP = os.getenv("TMP", "/tmp")
TMP = CWD/'data'
FNAME = 'movie_metadata.csv'
REMOTE = os.path.join(BASE_URL, FNAME)
# local = os.path.join(TMP, fname)
LOCAL = TMP/FNAME

MOVIE_DATA = LOCAL
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')


# Module
def get_data(remote: str=REMOTE, local: str=LOCAL):
    data_dir = TMP
    data_file = data_dir/FNAME

    if not data_dir.exists():
        print(f'Creating data directory ({data_dir})...')
        data_dir.mkdir()

    if not data_file.exists():
        print(f'Retrieving data and saving to {data_file}.')
        # Retrieve data_file:
        urlretrieve(remote, local)
    else:
        print(f'{data_file} already present.')


def get_movies_by_director():
    """Extracts all movies from csv and stores them in a dict,
    where keys are directors, and values are a list of movies,
    use the defined Movie namedtuple"""
    movies_by_dir = defaultdict(list)
    with open(MOVIE_DATA, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if all(
                row[val] for val in ('director_name', 'movie_title', 'title_year', 'imdb_score')
            ) and int(row['title_year']) >= MIN_YEAR:
                movie_title = row['movie_title'].rstrip('\xa0')
                movies_by_dir[row['director_name']].append(
                    Movie(movie_title, int(row['title_year']), float(row['imdb_score']))
                )

    return movies_by_dir


def calc_mean_score(movies):
    """Helper method to calculate mean of list of Movie namedtuples,
       round the mean to 1 decimal place"""
    return round(mean(movie.score for movie in movies), 1)


def get_average_scores(directors):
    """Iterate through the directors dict (returned by get_movies_by_director),
       return a list of tuples (director, average_score) ordered by highest
       score in descending order. Only take directors into account
       with >= MIN_MOVIES"""
    res = [
        (director, calc_mean_score(movies))
        for director, movies in directors.items()
        if len(movies) >= MIN_MOVIES
    ]
    # Better to use sorted - then don't need a variable:
    ## res.sort(key=lambda item: item[1], reverse=True)
    return sorted(res, key=lambda item: item[1], reverse=True)


if __name__ == '__main__':
    get_data()
    dirinfo = get_movies_by_director()
    with open(CWD/'dirinfo.json', mode='wt') as outfile:
        json.dump(dirinfo, outfile)

    dirscores = get_average_scores(dirinfo)
    with open(CWD/'dirscores.json', mode='wt') as outfile:
        json.dump(dirscores, outfile)

    count = 0
    res = pformat(dirscores)
    pprint(res.splitlines()[:20])
