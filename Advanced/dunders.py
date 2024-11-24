#! /usr/bin/env python3.13


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

    def __init__(self, name, start_balance=0):
        self.name = name
        self.start_balance = start_balance
        self._transactions = []

    @property
    def balance(self):
        return self.start_balance + sum(self._transactions)

    def __len__(self):
        return len(self._transactions)

    def __lt__(self, other):
        return self.balance < other.balance

    def __gt__(self, other):
        return self.balance > other.balance

    def __le__(self, other):
        return self.balance <= other.balance

    def __ge__(self, other):
        return self.balance >= other.balance

    def __eq__(self, other):
        return self.balance == other.balance

    def __ne__(self, other):
        return self.balance != other.balance
