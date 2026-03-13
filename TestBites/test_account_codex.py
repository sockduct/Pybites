#! /usr/bin/env python
"""Comprehensive pytest suite for the Account class.

This module verifies all behavior implemented in ``account.py``:
- object construction and defaults
- string and representation dunder methods
- transaction validation and storage
- computed balance property
- sequence protocol support (``len`` and index access)
- total ordering behavior provided by ``@total_ordering``
- account combination via ``__add__``
"""

from pathlib import Path
import sys

import pytest

# Make local module imports stable when tests are run from repository root.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from account import Account


@pytest.fixture
def empty_account() -> Account:
    """Return an account with a zero starting amount and no transactions."""
    return Account("George")


@pytest.fixture
def funded_account() -> Account:
    """Return an account with a non-zero starting amount and no transactions."""
    return Account("Jane", 10)


def test_init_with_default_amount() -> None:
    """Account initializes default amount and empty transaction history."""
    account = Account("George")
    assert account.owner == "George"
    assert account.amount == 0
    assert account._transactions == []


def test_init_with_explicit_amount() -> None:
    """Account initializes with an explicit starting amount."""
    account = Account("Jane", 50)
    assert account.owner == "Jane"
    assert account.amount == 50
    assert account._transactions == []


def test_repr_returns_unambiguous_object_representation(
    empty_account: Account, funded_account: Account
) -> None:
    """repr(Account) includes owner and starting amount as Python literals."""
    assert repr(empty_account) == "Account('George', 0)"
    assert repr(funded_account) == "Account('Jane', 10)"


def test_str_returns_human_readable_summary(
    empty_account: Account, funded_account: Account
) -> None:
    """str(Account) returns owner and initial amount in user-facing text."""
    assert str(empty_account) == "Account of George with starting amount: 0"
    assert str(funded_account) == "Account of Jane with starting amount: 10"


@pytest.mark.parametrize("invalid_amount", [5.5, "100", None, [1], {"amount": 1}])
def test_add_transaction_rejects_non_int_values(
    funded_account: Account, invalid_amount: object
) -> None:
    """Only integers are accepted as transactions; others raise ValueError."""
    with pytest.raises(ValueError, match="please use int for amount"):
        funded_account.add_transaction(invalid_amount)  # type: ignore[arg-type]


def test_add_transaction_accepts_int_and_appends(funded_account: Account) -> None:
    """Valid integer transactions are appended in order."""
    funded_account.add_transaction(7)
    funded_account.add_transaction(-3)
    assert funded_account._transactions == [7, -3]


def test_balance_is_start_amount_plus_all_transactions(funded_account: Account) -> None:
    """balance reflects starting amount and all signed transactions."""
    funded_account.add_transaction(20)
    funded_account.add_transaction(-5)
    assert funded_account.balance == 25


def test_len_returns_number_of_transactions(funded_account: Account) -> None:
    """len(Account) reports transaction count, not balance or start amount."""
    assert len(funded_account) == 0
    funded_account.add_transaction(1)
    funded_account.add_transaction(2)
    assert len(funded_account) == 2


def test_getitem_returns_transaction_by_index(funded_account: Account) -> None:
    """Account supports list-style transaction indexing via __getitem__."""
    funded_account.add_transaction(11)
    funded_account.add_transaction(-4)
    assert funded_account[0] == 11
    assert funded_account[1] == -4
    assert funded_account[-1] == -4


def test_getitem_raises_index_error_for_out_of_range(
    funded_account: Account,
) -> None:
    """Out-of-range index access mirrors list behavior and raises IndexError."""
    with pytest.raises(IndexError):
        _ = funded_account[0]


def test_total_ordering_comparisons() -> None:
    """All rich comparisons are derived correctly from balance."""
    low = Account("Low", 1)
    low.add_transaction(1)  # balance: 2
    high = Account("High", 5)
    high.add_transaction(1)  # balance: 6
    equal_to_high = Account("EqualHigh", 6)  # balance: 6

    assert high > low
    assert high >= equal_to_high
    assert low < high
    assert low <= high
    assert high == equal_to_high
    assert low != high


def test_add_combines_owner_start_amount_and_transactions() -> None:
    """Adding accounts returns a new account with merged state."""
    left = Account("George", 100)
    left.add_transaction(5)
    left.add_transaction(-10)

    right = Account("Jane", 25)
    right.add_transaction(30)

    merged = left + right

    assert isinstance(merged, Account)
    assert merged.owner == "George&Jane"
    assert merged.amount == 125
    assert list(merged) == [5, -10, 30]
    assert merged.balance == left.balance + right.balance


def test_add_does_not_mutate_original_accounts() -> None:
    """Combining accounts must not change source account transactions."""
    left = Account("Left", 0)
    right = Account("Right", 0)
    left.add_transaction(1)
    right.add_transaction(2)

    _ = left + right

    assert list(left) == [1]
    assert list(right) == [2]
