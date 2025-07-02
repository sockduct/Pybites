#! /usr/bin/env python3.13


import csv
import os
from pathlib import Path
import random
import sqlite3
import string
import sys
from typing import NamedTuple

import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))

from basetmpl import get_data, get_path


CWD = Path(__file__).parent
# Where to store retrieved data:
DATADIR = CWD/'data'
# Filename for retrieved data:
DATAFILE = 'UNDEFINED'
#
DATA_URL = 'https://query.data.world/s/ezwk64ej624qyverrw6x7od7co7ftm'
TMP = Path(os.getenv("TMP", "/tmp"))


class Player(NamedTuple):
    name: str
    year: int
    first_year: int
    team: str
    college: str
    active: bool
    games: int
    avg_min: float
    avg_points: float


class SQLiteDB:
    _instance = None
    _salt = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
    _db_path = DATADIR / f'nba_{_salt}.db'

    def __new__(cls, db_path=_db_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_connection(db_path)
        return cls._instance

    def _init_connection(self, db_path):
        self._db_path = db_path
        self._connection = sqlite3.connect(self._db_path)
        self._cursor = self._connection.cursor()

    def get_cursor(self):
        return self._cursor

    def commit(self):
        self._connection.commit()

    def close(self):
        self._cursor.close()
        self._connection.close()
        SQLiteDB._instance = None  # Allow reinitialization later

'''
# Usage Example
db = SQLiteCursorSingleton("my_database.db")
cursor = db.get_cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
db.commit()
db.close()
'''

def import_data():
    with requests.Session() as session:
        content = session.get(DATA_URL).content.decode('utf-8')

    reader = csv.DictReader(content.splitlines(), delimiter=',')

    players = []
    for row in reader:
        players.append(Player(name=row['Player'],
                              year=row['Draft_Yr'],
                              first_year=row['first_year'],
                              team=row['Team'],
                              college=row['College'],
                              active=row['Yrs'],
                              games=row['Games'],
                              avg_min=row['Minutes.per.Game'],
                              avg_points=row['Points.per.Game']))

    cur.execute('''CREATE TABLE IF NOT EXISTS players
                  (name, year, first_year, team, college, active,
                  games, avg_min, avg_points)''')
    cur.executemany('INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?)', players)
    conn.commit()


def player_with_max_points_per_game():
    """The player with highest average points per game (don't forget to CAST to
       numeric in your SQL query)"""
    pass


def number_of_players_from_duke():
    """Return the number of players with college == Duke University"""
    pass


def avg_years_active_players_stanford():
    """Return the average years that players from "Stanford University
       are active ("active" column)"""
    pass


def year_with_most_new_players():
    """Return the year with the most new players.
       Hint: you can use GROUP BY on the year column.
    """
    pass


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=False)

    import_data()
