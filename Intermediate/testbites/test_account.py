#! /usr/bin/env python
'''
In our third Test Bite you will write tests for (a reduced version of) the
Account class Bob wrote for his Enriching Your Python Classes With Dunder
(Magic, Special) Methods article
(https://dbader.org/blog/python-dunder-methods). You can assume Accounts to be
instantiated with integer amounts only.
'''


import pytest

from account import Account

# write your pytest functions below, they need to start with test_
'''
Testing:
* Test instantiation with and without optional argument
* Test str and repr dunder methods
* Test valid and invalid (non-int) transactions
* Test balance property
* Test length
* Test total ordering:  >, >=, <, <=, ==, !=
* Test add (creates new Account)
'''

@pytest.fixture
def acc1() -> Account:
    return Account('George')


@pytest.fixture
def acc2() -> Account:
    return Account('Jane', 10)


@pytest.mark.parametrize('owner, amount', {
    ('George', None),
    ('Jane', 10)
})
def test_account_init(owner, amount) -> None:
    acct = Account(owner, amount) if amount else Account(owner)
    assert acct.owner == owner
    if amount:
        assert acct.amount == amount
    else:
        assert acct.amount == 0
    assert acct._transactions == []


def test_account_repr(acc1: Account, acc2: Account) -> None:
    assert repr(acc1) == 'Account("George", 0)'
    assert repr(acc2) == 'Account("Jane", 10)'


def test_account_str(acc1: Account, acc2: Account) -> None:
    assert str(acc1) == 'Account of George with starting amount: 0'
    assert str(acc2) == 'Account of Jane with starting amount: 10'


@pytest.mark.parametrize('amount, expected', [
    (5.6, Exception),
    ('bad', ValueError),
    (7, None)
])
def test_account_trans(amount: int|float|str, expected: Exception|None, acc2: Account) -> None:
    assert acc2._transactions == []
    if isinstance(expected, Exception):
        with pytest.raises(ValueError):
            acc2.add_transaction(amount)
    else:
        acc2.add_transaction(amount)
        assert acc2._transactions == [amount]


def test_account_balance(acc2: Account) -> None:
    assert acc2.balance == 10
    acc2.add_transaction(20)
    assert acc2.balance == 30


def test_account_len(acc2: Account) -> None:
    assert len(acc2) == 0
    acc2.add_transaction(8)
    assert len(acc2) == 1
    acc2.add_transaction(15)
    assert len(acc2) == 2


def test_account_ordering(acc1: Account, acc2: Account) -> None:
    '''Test total ordering:  >, >=, <, <=, ==, !='''
    acc1.add_transaction(5)
    acc1.add_transaction(7)  # 12
    acc2.add_transaction(3)
    acc2.add_transaction(2)  # 15
    acc3 = Account('Beta', 15)
    assert acc2 > acc1
    assert acc2 >= acc3
    assert acc1 < acc2
    assert acc2 <= acc3
    assert acc2 == acc3
    assert acc1 != acc2


def test_account_add(acc1: Account, acc2: Account) -> None:
    acc1.add_transaction(5)
    acc1.add_transaction(7)
    acc2.add_transaction(3)
    acc3 = acc1 + acc2
    assert acc3.owner == f'{acc1.owner}&{acc2.owner}'
    assert acc3.balance == acc1.balance + acc2.balance
