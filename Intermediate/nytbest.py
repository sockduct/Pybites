#! /usr/bin/env python3.13
'''
In this Bite you are going to parse NY Times Best Seller Lists
(https://www.nytimes.com/books/best-sellers/hardcover-nonfiction) using The New
York Times Developer Network (https://developer.nytimes.com/).

This is the endpoint you will use:
https://api.nytimes.com/svc/books/v3/lists/current/hardcover-nonfiction.json?api-key=yourkey
(the tests also use hardcover-fiction.json).

Feel free to create an account and obtain an API key to try this out locally. To
work with static data we've mocked out the response in the tests.

Code get_best_seller_titles below, for the non-fiction best seller list, the
function should return the following list of tuples:
[
  ('BETWEEN THE WORLD AND ME', 86),
  ('EDUCATED', 79),
  ('BECOMING', 41),
  ('THE SECOND MOUNTAIN', 18),
  ('THE PIONEERS', 16),
  ('MAYBE YOU SHOULD TALK TO SOMEONE', 14),
  ('UNFREEDOM OF THE PRESS', 14),
  ('RANGE', 9),
  ('THREE WOMEN', 7),
  ('TRICK MIRROR', 3),
  ('HOW TO BE AN ANTIRACIST', 2),
  ('KOCHLAND', 2),
  ('THANK YOU FOR MY SERVICE', 1),
  ('THE OUTLAW OCEAN', 1),
  ('GODS OF THE UPPER AIR', 1)
]

Keep this script at hand, maybe you can run it in a few months and compare the
results. Or collect it weekly or monthly and start plotting the data?
'''


from operator import itemgetter
from pathlib import Path
from pprint import pprint
import requests
import sys
from types import ModuleType

# Local key override:
try:
    import keyring
    YOUR_KEY = keyring.get_password('NYTAPI', 'james.r.small@outlook.com')
except ImportError:
    YOUR_KEY = '123abc'


requests_cache: ModuleType | None
try:
    import requests_cache
except ImportError:
    requests_cache = None


DEFAULT_LIST = 'hardcover-nonfiction'
#
URL_NON_FICTION = (f'https://api.nytimes.com/svc/books/v3/lists/current/'
                   f'{DEFAULT_LIST}.json?api-key={YOUR_KEY}')
URL_FICTION = URL_NON_FICTION.replace('nonfiction', 'fiction')
#
CWD = Path(__file__).parent
DATA = CWD/'data'
TESTING = 'pytest'


def get_best_seller_titles(url: str=URL_NON_FICTION) -> list[tuple[str, int]]:
    """Use the NY Times Books API endpoint above to get the titles that are
       on the best seller list for the longest time.

       Return a list of (title, weeks_on_list) tuples, e.g. for the nonfiction:

       [('BETWEEN THE WORLD AND ME', 86),
        ('EDUCATED', 79),
        ('BECOMING', 41),
        ('THE SECOND MOUNTAIN', 18),
         ... 11 more ...
       ]

       Dev docs: https://developer.nytimes.com/docs/books-product/1/overview
    """
    if TESTING not in sys.modules and requests_cache:
        requests_cache.install_cache('pybites-s3-cache')

    category = 'Non-fiction' if url == URL_NON_FICTION else 'Fiction'
    resp = requests.get(url)
    resp.raise_for_status()

    data = resp.json()

    # Save:
    if TESTING not in sys.modules:
        current = data['results']['bestsellers_date']
        file = DATA/f'nyt-{category}-{current}.json'
        if not file.exists():
            print(f'Saving results for {category} for {current} to {DATA}...')
            file.write_text(resp.text)

    return sorted(
        ((book['title'], book['weeks_on_list']) for book in data['results']['books']),
        key=itemgetter(1),
        reverse=True
    )


if __name__ == '__main__':
    for url in (URL_NON_FICTION, URL_FICTION):
        ret = get_best_seller_titles(url)
        pprint(ret)
