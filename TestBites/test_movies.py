'''
Time for fixtures, one of pytest's killer features or as Brian Okken said:
pytest fixtures are one of the unique core features that make pytest stand out
above other test frameworks, and are the reason why many people switch to and
stay with pytest (Python Testing with pytest).

Why fixtures? The purpose of test fixtures is to provide a fixed baseline upon
which tests can reliably and repeatedly execute. pytest fixtures offer dramatic
improvements over the classic xUnit style of setup/teardown functions (docs).

In this Bite we wrote a little movie DB using sqlite3. The idea is that you
write a db fixture to instantiate this class and run its init method to get the
movies table created and populated. At the end of the fixture you use drop_table
to undo any changes.

Apart from this setup and teardown there are 3 methods you need to test: query,
add and delete. Specially query has various args, so make sure you test them all.

Apart from the docs (https://docs.pytest.org/en/latest/fixture.html) we also
wrote an article on fixtures you might want to check out: All You Need to Know
to Start Using Fixtures in Your pytest Code
(https://pybit.es/articles/pytest-fixtures/).

Let us know on Twitter when you finish our pytest learning path ... Good luck
and keep calm and code in Python / pytest!
'''


import os
from pathlib import Path
import random
import re
import string
import sys
from typing import Generator

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest

from movies import MovieDb

salt = ''.join(random.choice(string.ascii_lowercase) for _ in range(20))
DB = os.path.join(os.getenv("TMP", "/tmp"), f'movies_{salt}.db')
# https://www.imdb.com/list/ls055592025/
DATA = [
    ("The Godfather", 1972, 9.2),
    ("The Shawshank Redemption", 1994, 9.3),
    ("Schindler's List", 1993, 8.9),
    ("Raging Bull", 1980, 8.2),
    ("Casablanca", 1942, 8.5),
    ("Citizen Kane", 1941, 8.3),
    ("Gone with the Wind", 1939, 8.1),
    ("The Wizard of Oz", 1939, 8),
    ("One Flew Over the Cuckoo's Nest", 1975, 8.7),
    ("Lawrence of Arabia", 1962, 8.3),
]
TABLE = 'movies'


@pytest.fixture
def db() -> Generator[MovieDb, None, None]:
    # instantiate MovieDb class using above constants
    # do proper setup / teardown using MovieDb methods
    # https://docs.pytest.org/en/latest/fixture.html (hint: yield)
    # Setup:
    movie_db = MovieDb(DB, DATA, TABLE)
    movie_db.init()

    yield movie_db

    # Teardown
    movie_db.drop_table()
    movie_db.con.close()


# write tests for all MovieDb's query / add / delete
def test_query(db: MovieDb) -> None:
    '''
    Matrix of possible query values:
    Title | Year | Score  | Notes
    ------+------+--------+---------------------------------
    None  | None | None   |
    ------+------+--------+---------------------------------
    <str> + None + None   |
    ------+------+--------+---------------------------------
    None  + <int>+ None   |
    ------+------+--------+---------------------------------
    None  + None + <float>|
    ------+------+--------+---------------------------------
    <str> + <int>+ None   | Multiple values not supported...
    ------+------+--------+---------------------------------
    <str> + None + <float>| Multiple values not supported...
    ------+------+--------+---------------------------------
    <str> + <int>+ <float>| Multiple values not supported...
    ------+------+--------+---------------------------------
    None  + <int>+ <float>| Multiple values not supported...
    '''
    # None, None, None:
    assert len(db.query()) == len(DATA)
    # <str>, None, None:
    assert len(db.query('the')) == sum(
        re.search(r'\b[Tt]he\b', datum[0]) is not None for datum in DATA
    )
    # None, <int>, None:
    assert len(db.query(year=1939)) == sum(datum[1] == 1939 for datum in DATA)
    # None, None, <float>:
    assert len(db.query(score_gt=9.0)) == sum(datum[2] >= 9.0 for datum in DATA)

def _add_movie(db: MovieDb) -> tuple[int|None, str|None, int, float]:
    new_movie = ('Vertigo', 1958, 8.2)
    new_id = db.add(*new_movie)
    return (new_id, *new_movie)

def test_add(db: MovieDb) -> None:
    assert len(db.query()) == len(DATA)
    new_row = _add_movie(db)
    assert len(db.query()) == len(DATA) + 1
    new_query = db.query(new_row[1])
    assert len(new_query) == 1
    assert new_query[0][0] == new_row[0]

def test_delete(db: MovieDb) -> None:
    new_row = _add_movie(db)
    assert len(db.query()) == len(DATA) + 1
    db.delete(new_row[0])
    assert len(db.query()) == len(DATA)

'''
Solution tests:
def test_inserted_data(db):
    rows = db.query()
    assert len(rows) == 10
    assert rows[0] == (1, 'The Godfather', 1972, 9.2)


def test_query_by_title(db):
    rows = db.query(title='Nest')
    assert rows == [(9, "One Flew Over the Cuckoo's Nest", 1975, 8.7)]
    rows = db.query(title='aw')
    assert rows == [(2, 'The Shawshank Redemption', 1994, 9.3),
                    (10, 'Lawrence of Arabia', 1962, 8.3)]


def test_query_by_year(db):
    rows = db.query(year=1972)
    assert rows == [(1, 'The Godfather', 1972, 9.2)]
    rows = db.query(year=1939)
    assert rows == [(7, 'Gone with the Wind', 1939, 8.1),
                    (8, 'The Wizard of Oz', 1939, 8.0)]


def test_query_by_score(db):
    rows = db.query(score_gt=9)
    assert rows == [(1, 'The Godfather', 1972, 9.2),
                    (2, 'The Shawshank Redemption', 1994, 9.3)]


def test_add(db):
    new_rowid = db.add('Scarface', 1983, 8.3)
    rows = db.query()
    assert len(rows) == new_rowid == 11
    assert rows[-1] == (11, 'Scarface', 1983, 8.3)


def test_delete(db):
    rows = db.query()
    assert len(rows) == 10
    assert (1, 'The Godfather', 1972, 9.2) in rows
    db.delete(1)
    rows = db.query()
    assert len(rows) == 9
    assert (1, 'The Godfather', 1972, 9.2) not in rows
'''
