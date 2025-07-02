from pathlib import Path
import sys
from time import time

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fibonacci import cached_fib


N = 30


def nocache_fib(n):
    if n < 2:
        return n
    return nocache_fib(n - 1) + nocache_fib(n - 2)


def _run(func):
    start = time()
    ret = func(N)
    end = time()
    return ret, end - start


@pytest.fixture(scope='module')
def not_cached():
    return _run(nocache_fib)


@pytest.fixture(scope='module')
def cached():
    return _run(cached_fib)


def test_correct_fibonacci(cached):
    ret, _ = cached
    err = 'Did not assert fibonacci return for n=30'
    assert ret == 832040, err


def test_cached_faster_than_non_cached(not_cached, cached):
    _, t1 = not_cached
    _, t2 = cached
    err = 'Cached version is not at least 10x faster'
    assert t2 < t1/10, err
