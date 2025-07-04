#! /usr/bin/env python3.13


import atexit
import csv
import os
from pathlib import Path
import random
import sqlite3
import string
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import cast, NamedTuple, Optional

import requests
requests_cache: ModuleType | None
try:
    import requests_cache
except ImportError:
    requests_cache = None


DATA_URL = 'https://query.data.world/s/ezwk64ej624qyverrw6x7od7co7ftm'
TMP = Path(os.getenv('TMP', '/tmp'))


class Player(NamedTuple):
    name: str
    year: int
    first_year: int
    team: str
    college: str
    active: int
    games: int
    avg_min: float
    avg_points: float


class SQLiteDB:
    _instance: Optional['SQLiteDB'] = None
    _salt: str = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
    _tempdir: TemporaryDirectory[str] = TemporaryDirectory()
    _db_path: Path = Path(_tempdir.name) / f'nba_{_salt}.db'

    def __new__(cls, db_path: Path=_db_path) -> 'SQLiteDB':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_connection(db_path)
        return cls._instance

    def __repr__(self) -> str:
        return f'SQLiteDB({self._db_path})'

    def _init_connection(self, db_path: Path) -> None:
        self._db_path = db_path
        self._connection = sqlite3.connect(self._db_path)
        self._cursor = self._connection.cursor()

    def get_cursor(self) -> sqlite3.Cursor:
        return self._cursor

    def commit(self) -> None:
        self._connection.commit()

    def close(self) -> None:
        self._cursor.close()
        self._connection.close()
        SQLiteDB._instance = None  # Allow reinitialization later
        SQLiteDB._tempdir.cleanup()


@atexit.register
def cleanup() -> None:
    if SQLiteDB._instance:
        db = SQLiteDB()
        db.close()


def import_data() -> None:
    if requests_cache:
        requests_cache.install_cache('pybites-s3-cache')
    with requests.Session() as session:
        content = session.get(DATA_URL).content.decode('utf-8')

    reader = csv.DictReader(content.splitlines(), delimiter=',')

    players: list[Player] = []
    players.extend(
        Player(
            name=row['Player'],
            year=int(row['Draft_Yr']),
            first_year=int(row['first_year']),
            team=row['Team'],
            college=row['College'],
            active=int(row['Yrs']),
            games=int(row['Games']),
            avg_min=float(row['Minutes.per.Game']),
            avg_points=float(row['Points.per.Game']),
        )
        for row in reader
    )

    db = SQLiteDB()
    cur = db.get_cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS players
        (name, year, first_year, team, college, active, games, avg_min, avg_points)
    ''')
    cur.executemany('INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', players)
    db.commit()


def player_with_max_points_per_game() -> str:
    """The player with highest average points per game (don't forget to CAST to
       numeric in your SQL query)"""
    cur = SQLiteDB().get_cursor()
    # Alternatively:  'SELECT name, max(CAST(avg_points AS decimal)) FROM players'
    cur.execute('select name from players order by avg_points desc limit 1;')
    return cast(str, cur.fetchone()[0])


def number_of_players_from_duke() -> int:
    """Return the number of players with college == Duke University"""
    cur = SQLiteDB().get_cursor()
    cur.execute('select count(*) from players where college = "Duke University";')
    return cast(int, cur.fetchone()[0])


def avg_years_active_players_stanford() -> float:
    """Return the average years that players from "Stanford University
       are active ("active" column)"""
    cur = SQLiteDB().get_cursor()
    cur.execute('select avg(active) from players where college = "Stanford University";')
    return cast(float, cur.fetchone()[0])


def year_with_most_new_players() -> int:
    """Return the year with the most new players.
       Hint: you can use GROUP BY on the year column.
    """
    cur = SQLiteDB().get_cursor()
    cur.execute('select year, count(*) from players group by year order by count(*) desc')
    return cast(int, cur.fetchone()[0])


# Singleton, so OK:
db = SQLiteDB()
cur = db.get_cursor()

# Need to always run the way the tests are designed:
import_data()


if __name__ == '__main__':
    # Originally used try/finally to handle database/tempdir cleanup but doesn't
    # work when called from pytest/nbasql_test.py - switched to atexit

    # Test:
    print(f'{player_with_max_points_per_game()=}')
    print(f'{number_of_players_from_duke()=}')
    print(f'{avg_years_active_players_stanford()=:.2f}')
    print(f'{year_with_most_new_players()=}')
