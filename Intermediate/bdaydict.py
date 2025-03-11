#! /usr/bin/env python3.13


from collections import UserDict
from datetime import date, datetime


MSG = 'Hey {}, there are more people with your birthday!'


class BirthdayDict(dict[str, date|datetime]):
    """Override dict to print a message every time a new person is added that has
       the same birthday (day+month) as somebody already in the dict"""

    def __setitem__(self, name: str, birthday: date|datetime) -> None:
        '''
        # Original:
        if birthday in self.values() or (
            (birthday.month, birthday.day) in {(val.month, val.day) for val in self.values()}
        ):
        '''
        # Better - don't need to check for year and allow short circuiting:
        if any((birthday.month, birthday.day) == (val.month, val.day) for val in self.values()):
            print(MSG.format(name))
        super().__setitem__(name, birthday)


class BirthdayDict2(UserDict[str, date|datetime]):
    def __setitem__(self, name: str, birthday: date|datetime) -> None:
        if any((birthday.month, birthday.day) == (val.month, val.day) for val in self.values()):
            print(MSG.format(name))
        super().__setitem__(name, birthday)


if __name__ == '__main__':
    print('Working with subclassed dict:')
    bd = BirthdayDict()
    bd['bob'] = date(1987, 6, 15)
    bd['tim'] = date(1984, 7, 15)
    bd['mary'] = date(1987, 6, 15)  # whole date match
    bd['sara'] = date(1987, 6, 14)
    bd['mike'] = date(1981, 7, 15)  # day + month match

    # Issue with subclassing dict:
    # Does NOT trigger __setitem__, because dict.update() bypasses __setitem__!
    bd.update({'jeff': date(1987, 6, 15)})

    print('\nWorking with subclassed UserDict:')
    # Subclassing UserDict:
    bd2 = BirthdayDict2()
    bd2['bob'] = date(1987, 6, 15)
    bd2['tim'] = date(1984, 7, 15)
    bd2['mary'] = date(1987, 6, 15)  # whole date match
    # Subclassing UserDict, works as expected:
    bd2.update({'jeff': date(1987, 6, 15)})
