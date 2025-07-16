import inspect
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from helplen import get_len_help_text


def test_pow():
    assert get_len_help_text(pow) == 280


def test_max():
    assert get_len_help_text(max) == 398


def test_bad_input():
    max1 = object()
    with pytest.raises(ValueError):
        get_len_help_text(max1)


def test_another_bad_input():
    with pytest.raises(ValueError):
        get_len_help_text('string')


def test_src():
    src = inspect.getsource(get_len_help_text)
    assert 'help' in src
    assert 'redirect_stdout' in src
