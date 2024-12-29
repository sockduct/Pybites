#! /usr/bin/env python3.13


from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar


P = ParamSpec('P')  # Function parameter types
R = TypeVar('R')    # Function return type


known_users = ['bob', 'julian', 'mike', 'carmen', 'sue']
loggedin_users = ['mike', 'sue']


def login_required(func: Callable[P, R]) -> Callable[P, R|str]:
    '''
    Leverage known_users and loggedin_users for "session management"

    Must account for following three scenarios:
    1) user is not on the system, return "please create an account"
    2) user is on the system but not logged in, return "please login"
    3) user is on the system and logged in, return the function's "welcome back
       {user}"
    '''
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R|str:
        user = args[0]
        if user not in known_users:
            # return f'User {user} unknown - please create an account.'
            return 'please create an account'
        elif user in loggedin_users:
            return func(*args, **kwargs)
        else:
            # return f'User {user} logged out - please login.'
            return 'please login'

    return wrapper


@login_required
def welcome(user: str) -> str:
    '''Return a welcome message if logged in'''
    return f'welcome back {user}'


if __name__ == '__main__':
    for user in ('lorne', 'bob', 'sue'):
        print(welcome(user))
