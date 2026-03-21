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

def test_add(db: MovieDb) -> None:
    ...

def test_delete(db: MovieDb) -> None:
    ...
