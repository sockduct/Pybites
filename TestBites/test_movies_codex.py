import importlib.util
from pathlib import Path
import sqlite3

import pytest


MODULE_PATH = Path(__file__).with_name("movies.py")
SPEC = importlib.util.spec_from_file_location("movies_under_test", MODULE_PATH)
movies = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(movies)
MovieDb = movies.MovieDb


@pytest.fixture
def sample_data():
    return [
        ("The Matrix", 1999, 8.7),
        ("The Godfather", 1972, 9.2),
        ("Toy Story", 1995, 8.3),
        ("The Matrix Reloaded", 2003, 7.2),
    ]


@pytest.fixture
def movie_db(sample_data):
    db = MovieDb(":memory:", sample_data, "movies")
    db.init()
    return db


def test_init_creates_table_and_inserts_sample_data(movie_db, sample_data):
    rows = movie_db.query()

    assert len(rows) == len(sample_data)
    assert [row[1:] for row in rows] == sample_data


def test_create_table_is_idempotent(sample_data):
    db = MovieDb(":memory:", sample_data, "movies")

    db._create_table()
    db._create_table()

    db.cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='movies'"
    )
    assert db.cur.fetchone() == ("movies",)


def test_query_without_filters_returns_all_rows(movie_db, sample_data):
    assert movie_db.query() == [
        (1, *sample_data[0]),
        (2, *sample_data[1]),
        (3, *sample_data[2]),
        (4, *sample_data[3]),
    ]


def test_query_by_title_uses_partial_match(movie_db):
    rows = movie_db.query(title="Matrix")

    assert rows == [
        (1, "The Matrix", 1999, 8.7),
        (4, "The Matrix Reloaded", 2003, 7.2),
    ]


def test_query_by_year_returns_exact_matches(movie_db):
    assert movie_db.query(year=1972) == [
        (2, "The Godfather", 1972, 9.2),
    ]


def test_query_by_score_gt_returns_only_higher_scores(movie_db):
    assert movie_db.query(score_gt=8.5) == [
        (1, "The Matrix", 1999, 8.7),
        (2, "The Godfather", 1972, 9.2),
    ]


def test_query_prioritizes_title_over_other_filters(movie_db):
    rows = movie_db.query(title="Toy", year=1972, score_gt=9.0)

    assert rows == [
        (3, "Toy Story", 1995, 8.3),
    ]


def test_query_prioritizes_year_over_score_when_title_missing(movie_db):
    rows = movie_db.query(year=2003, score_gt=9.0)

    assert rows == [
        (4, "The Matrix Reloaded", 2003, 7.2),
    ]


def test_add_returns_new_row_id_and_row_is_queryable(movie_db):
    row_id = movie_db.add("Inception", 2010, 8.8)

    assert row_id == 5
    assert movie_db.query(title="Inception") == [
        (5, "Inception", 2010, 8.8),
    ]


def test_delete_removes_row_from_subsequent_queries(movie_db):
    movie_db.delete(2)

    assert movie_db.query(year=1972) == []
    assert [row[0] for row in movie_db.query()] == [1, 3, 4]


def test_drop_table_removes_table(movie_db):
    movie_db.drop_table()

    with pytest.raises(sqlite3.OperationalError):
        movie_db.query()
