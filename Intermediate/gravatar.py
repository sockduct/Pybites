#! /usr/bin/env python3.13
'''
In this Bite you will generate a Gravatar URL, e.g.
https://www.gravatar.com/avatar/5b13356d467af88631503c27a3d0e0cf?s=200&r=g&d=robohash.

In this URL 5b13356d467af88631503c27a3d0e0cf is a hash of a lowercase and
stripped email address.

Code create_gravatar_url hashing the passed in email arg. You can see a PHP
example (https://en.gravatar.com/site/implement/hash/) and you want to use
hashlib + its md5 / hexdigest methods
(https://docs.python.org/3/library/hashlib.html#hashlib.hash.hexdigest)...

Here is how the function works in the REPL. Note that spaces and case
sensitivity won't matter: they produce the same hash and thus gravatar:

>>> from gravatar import create_gravatar_url
>>> create_gravatar_url("bob@pybit.es")
'https://www.gravatar.com/avatar/5b13356d467af88631503c27a3d0e0cf?s=200&r=g&d=robohash'
>>> create_gravatar_url("bob@pybit.es", 300)
'https://www.gravatar.com/avatar/5b13356d467af88631503c27a3d0e0cf?s=300&r=g&d=robohash'
>>> create_gravatar_url("bob@pybit.es ", 300)
'https://www.gravatar.com/avatar/5b13356d467af88631503c27a3d0e0cf?s=300&r=g&d=robohash'
>>> create_gravatar_url("bob@pybit.ES ", 300)
'https://www.gravatar.com/avatar/5b13356d467af88631503c27a3d0e0cf?s=300&r=g&d=robohash'
(More information about the other parameters here
{https://en.gravatar.com/site/implement/images/})
'''


import hashlib

GRAVATAR_URL = ("https://www.gravatar.com/avatar/"
                "{hashed_email}?s={size}&r=g&d=robohash")


def create_gravatar_url(email: str, size: int=200) -> str:
    """Use GRAVATAR_URL above to create a gravatar URL.

       You need to create a hash of the email passed in.

       PHP example: https://en.gravatar.com/site/implement/hash/

       For Python check hashlib check out (md5 / hexdigest):
       https://docs.python.org/3/library/hashlib.html#hashlib.hash.hexdigest
    """
    # email_bytes = bytes(email.lower().strip(), encoding='utf8')
    # Prefer this:
    email_bytes = email.lower().strip().encode('utf8')
    email_md5hd = hashlib.md5(email_bytes).hexdigest()
    return GRAVATAR_URL.format(hashed_email=email_md5hd, size=size)


if __name__ == '__main__':
    for *args, expected in (
        ("bob@pybit.es",
         'https://www.gravatar.com/avatar/5b13356d467af88631503c27a3d0e0cf?s=200&r=g&d=robohash'),
        ("bob@pybit.es", 300,
         'https://www.gravatar.com/avatar/5b13356d467af88631503c27a3d0e0cf?s=300&r=g&d=robohash'),
        ("bob@pybit.es ", 300,
         'https://www.gravatar.com/avatar/5b13356d467af88631503c27a3d0e0cf?s=300&r=g&d=robohash'),
        ("bob@pybit.ES ", 300,
         'https://www.gravatar.com/avatar/5b13356d467af88631503c27a3d0e0cf?s=300&r=g&d=robohash')
    ):
        print(f'\nInvoking create_gravatar_url with {args}...')
        # Could fix but kludgey and this is elegant:
        result = create_gravatar_url(*args)  # type: ignore
        print(f'{result} =?=\n{expected}')
        assert result == expected
