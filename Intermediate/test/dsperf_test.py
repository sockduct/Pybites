from pathlib import Path
from string import ascii_lowercase
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from dsperf import (contains, contains_fast,
                    ordered_list_max, ordered_list_max_fast,
                    list_concat, list_concat_fast,
                    list_inserts, list_inserts_fast,
                    list_creation, list_creation_fast)


alist = list(range(1_000_000))
aset = set(alist)
listofstrings = list(ascii_lowercase) * 1_000


def test_contains():
    t1, res1 = contains(alist, 500)
    t2, res2 = contains_fast(aset, 1_000)
    assert res1 == res2
    assert t1 > t2


def test_ordered_max():
    t1, res1 = ordered_list_max(alist)
    t2, res2 = ordered_list_max_fast(alist)
    assert res1 == res2
    assert t1 > t2


def test_concat():
    t1, res1 = list_concat(listofstrings)
    t2, res2 = list_concat_fast(listofstrings)
    assert res1 == res2
    assert t1 > t2


def test_list_insert():
    t1, res1 = list_inserts(10_000)
    t2, res2 = list_inserts_fast(10_000)
    assert list(res1) == list(res2)
    assert t1 > t2


def test_list_creation():
    t1, res1 = list_creation(10_000)
    t2, res2 = list_creation_fast(10_000)
    assert list(res1) == list(res2)
    assert t1 > t2
