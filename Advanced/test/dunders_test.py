from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).parent.parent))


from dunders import Account


@pytest.fixture
def checking():
    return Account("Checking")


@pytest.fixture
def checking_with_start_balance():
    return Account("Checking", 10)


@pytest.fixture
def checking_with_more_start_balance():
    return Account("Checking", 15)


@pytest.fixture
def saving():
    return Account("Saving", 10)


@pytest.fixture
def saving_less():
    return Account("Saving", 5)


def test_account_balance(checking, saving):
    assert checking.start_balance == 0
    checking + 10
    assert checking.balance == 10

    assert saving.start_balance == 10
    with pytest.raises(TypeError):
        saving - "a"
    saving - 5
    assert saving.balance == 5


def test_account_comparison(checking_with_start_balance, saving_less):
    assert checking_with_start_balance > saving_less
    assert checking_with_start_balance >= saving_less
    assert saving_less < checking_with_start_balance
    assert saving_less <= checking_with_start_balance
    saving_less + 5
    assert checking_with_start_balance == saving_less


def test_account_len(checking):
    checking + 10
    checking + 3
    checking - 8
    assert len(checking) == 3


def test_account_indexing_iter(checking):
    checking + 10
    checking + 10
    checking + 3
    checking - 8
    assert checking[0] == 10
    assert checking[-1] == -8
    assert list(checking) == [10, 10, 3, -8]


def test_account_str(checking_with_more_start_balance, saving):
    assert str(checking_with_more_start_balance) == "Checking account - balance: 15"
    assert str(saving) == "Saving account - balance: 10"
    saving + 5
    assert str(saving) == "Saving account - balance: 15"
