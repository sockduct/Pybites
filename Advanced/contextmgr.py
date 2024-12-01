#! /usr/bin/env python3.13


from types import TracebackType
from typing import Self, Type


# Types:
numeric = int | float


class Account:
    def __init__(self) -> None:
        self._transactions: list[numeric] = []

    @property
    def balance(self) -> numeric:
        return sum(self._transactions)

    def __add__(self, amount: numeric) -> None:
        self._transactions.append(amount)

    def __sub__(self, amount: numeric) -> None:
        self._transactions.append(-amount)

    # add 2 dunder methods here to turn this class
    # into a 'rollback' context manager
    def __enter__(self) -> Self:
        self._save_transactions = self._transactions.copy()
        return self

    def __exit__(self, exc_type: Type[BaseException]|None, exc_value: BaseException|None,
                 traceback: TracebackType|None) -> None:
        # Rollback if balance negative:
        if self.balance < 0:
            # May want notification:
            print('Balance below 0, rolling back transaction(s)...')
            self._transactions = self._save_transactions
