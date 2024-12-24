#! /usr/bin/env python3.13


from pathlib import Path

import pytest


cwd = Path(__file__).parent
target_test = 'pubdates_test.py'
pytest.main(['-v', cwd/'Intermediate'/'test'/target_test])
