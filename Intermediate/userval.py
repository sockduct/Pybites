#! /usr/bin/env python3.13

from collections import namedtuple

User = namedtuple('User', 'name role expired')
USER, ADMIN = 'user', 'admin'
SECRET = 'I am a very secret token'

julian = User(name='Julian', role=USER, expired=False)
bob = User(name='Bob', role=USER, expired=True)
pybites = User(name='PyBites', role=ADMIN, expired=False)
USERS = (julian, bob, pybites)

# define exception classes here
class UserDoesNotExist(Exception):
    pass

class UserAccessExpired(Exception):
    pass

class UserNoPermission(Exception):
    pass

def get_secret_token(username: str) -> str:
    '''
    Validation:
    1. The username is in USERS
    2. The user's account has not expired.
    3. The user has the ADMIN role.

    Yes:  return SECRET
    No:   raise either UserDoesNotExist, UserAccessExpired or UserNoPermission
    '''
    if not (user := [user for user in USERS if user.name == username]):
        raise UserDoesNotExist
    if user[0].expired:
        raise UserAccessExpired
    if user[0].role != ADMIN:
        raise UserNoPermission

    return SECRET
