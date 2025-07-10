from pathlib import Path
import sys
from types import NoneType
from typing import get_type_hints

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from class_typing1 import Employee


@pytest.fixture(scope="module")
def employee():
    return Employee("Mohhinder", "Suresh", 5, 8, 12.75)


# def test_employee_type_hints(employee):
def test_employee_type_hints():
    # actual = get_type_hints(employee)
    actual = get_type_hints(Employee.__init__)
    expected_type_hints = {
        "first_name": str,
        "last_name": str,
        "days_per_week": int,
        "hours_per_day": float,
        "wage": float,
        "return": NoneType,  # imported from types
    }
    assert actual == expected_type_hints


def test_rounder_type_hints(employee):
    actual = get_type_hints(employee._rounder)
    expected_type_hints = {
        "number": float,
        "places": int,
        "return": str,
    }
    assert actual == expected_type_hints


def test_weekly_pay(employee):
    assert isinstance(employee.weekly_pay, str)
