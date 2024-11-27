#! /usr/bin/env python3.13


from functools import total_ordering
from typing import Iterator, Self


numeric = int | float


@total_ordering
class Account:
    '''
    Dunder methods - implement the following:
    * len returns # of transactions
    * comparison operations (==, !=, <, >, <=, >=) return boolean comparing account
    balances
    * indexing returns nth transaction on account
    * iteration returns sequence of account transactions
    * +/- int adds/subtracts money (raise TypeError if wrong type)
    * str returns:  NAME account - balance: INT
    '''

    def __init__(self, name: str, start_balance: numeric=0) -> None:
        self.name = name
        self.start_balance = start_balance
        self._transactions: list[numeric] = []

    @property
    def balance(self) -> numeric:
        return self.start_balance + sum(self._transactions)

    def __len__(self) -> int:
        return len(self._transactions)

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, Account):
            return NotImplemented

        return self.balance < other.balance

    # Could skip and use functools.total_ordering but slower:
    '''
    def __gt__(self, other: Self) -> bool:
        if not isinstance(other, Account):
            return NotImplemented

        return self.balance > other.balance

    # Could skip and use functools.total_ordering but slower:
    def __le__(self, other: Self) -> bool:
        if not isinstance(other, Account):
            return NotImplemented

        return self.balance <= other.balance

    # Could skip and use functools.total_ordering but slower:
    def __ge__(self, other: Self) -> bool:
        if not isinstance(other, Account):
            return NotImplemented

        return self.balance >= other.balance
    '''

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return NotImplemented

        return self.balance == other.balance

    # Could skip and use functools.total_ordering but slower:
    '''
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return NotImplemented

        return self.balance != other.balance
    '''

    def __getitem__(self, index: int) -> numeric:
        return self._transactions[index]

    # Not strictly necessary because __getitem__ is implemented:
    def __iter__(self) -> Iterator[numeric]:
        return iter(self._transactions)

    def _validate(self, amount: numeric) -> None:
        if not isinstance(amount, (int, float)):
            raise TypeError(f'Amount must be int or float, not {type(amount)}')

    def __add__(self, amount: numeric) -> Self:
        self._validate(amount)
        self._transactions.append(amount)
        return self

    def __sub__(self, amount: numeric) -> Self:
        self._validate(amount)
        self._transactions.append(-amount)
        return self

    def __str__(self) -> str:
        return f'{self.name} account - balance: {self.balance}'
