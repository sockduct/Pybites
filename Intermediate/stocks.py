#! /usr/bin/env python3.13
'''
In this Bite we will answer some questions about stocks, using some JSON data
obtained from the awesome Mockeroo fake data generator service
(https://www.mockaroo.com/).

Here is a snippet of the output you will parse (full output at STOCK_DATA):
[
  {
    "id": 1,
    "name": "Anworth Mortgage Asset Corporation",
    "symbol": "ANH",
    "industry": "Real Estate Investment Trusts",
    "sector": "Consumer Services",
    "market": "NYSE",
    "cap": "$600.57M"
  },
  {
    "id": 2,
    "name": "DarioHealth Corp.",
    "symbol": "DRIO",
    "industry": "Medical/Dental Instruments",
    "sector": "Health Care",
    "market": "NASDAQ",
    "cap": "$21.78M"
  },
   ...998 more stocks...
]

Complete the 4 functions below following the instructions in the docstrings.
Good luck and keep calm and parse your Data in Python.
'''


from collections import Counter
import json
from pathlib import Path
from pprint import pprint, PrettyPrinter
from textwrap import fill
from typing import Literal, TypedDict, cast

import requests


STOCK_DATA = 'https://bites-data.s3.us-east-2.amazonaws.com/stocks.json'
#
# Defining data as global only because bite setup that way:
data = None
#
CWD = Path(__file__).parent
# Where to store retrieved data:
DATADIR = CWD/'data'
# Filename for retrieved data:
DATAFILE = 'stocks.json'


# Types
class Stock(TypedDict):
    id: int
    name: str
    symbol: str
    industry: str
    sector: str
    market: str
    cap: str

type StockKey = Literal['id', 'name', 'symbol', 'industry', 'sector', 'market', 'cap']


def _get_data(verbose: bool=False) -> list[Stock]:
    # Not recommended - doing because bite setup this way:
    global data
    cached = DATADIR/DATAFILE

    # Check if already loaded:
    if not data:
        # Load JSON data into program:
        if cached.is_file():
            if verbose:
                print(f'Loading data from cached file "{cached}"...')
            with cached.open('r', encoding='utf8') as fp:
                data = json.load(fp)
        else:
            if verbose:
                print(f'Retrieving data from source "{STOCK_DATA}"...')
            with requests.Session() as s:
                data = s.get(STOCK_DATA).json()
            if verbose:
                print(f'Saving data to local cached file "{cached}"...')
            with cached.open('w', encoding='utf8') as fp:
                json.dump(data, fp)

    return cast(list[Stock], data)


def _cap_str_to_mln_float(cap: str) -> float:
    """If cap = 'n/a' return 0, else:
       - strip off leading '$',
       - if 'M' in cap value, strip it off and return value as float,
       - if 'B', strip it off, multiply by 1,000 and return
         value as float"""
    if cap.lower() == 'n/a':
        return 0

    cap = cap.strip('$')
    if cap.endswith('M'):
        return float(cap.strip('M'))
    elif cap.endswith('B'):
        return float(cap.strip('B')) * 1_000
    else:
        raise ValueError(f'Unexpected market cap value:  "{cap}"')


def get_values(field: StockKey) -> None|str:
    '''
    Return a sorted list of all unique values present in field in data set.
    e.g., Show all possible markets.
    '''
    local_data = _get_data()
    valid_keys = set(Stock.__annotations__.keys())
    for invalid_key in ('id', 'cap', 'name', 'symbol'):
        valid_keys.remove(invalid_key)
    valid_fields = ', '.join(sorted(valid_keys))
    if field == 'id':
        print(f'Valid fields:  {valid_fields} ("id" is a unique identifier '
              'and not eligible)')
        return None
    elif field in {'cap', 'name', 'symbol'}:
        print(f'Valid fields:  {valid_fields} ("{field}" is a per-stock value '
              'and not eligible)')
        return None
    elif field not in valid_keys:
        raise ValueError(f'Invalid field:  "{field}", expected one of:  {valid_fields}')

    # Textwrap appears to be more flexible and doesn't wrap output in a tuple
    # pretty = PrettyPrinter(compact=True)
    # return pretty.pformat(', '.join(sorted(result)))
    if  result:= {
        cast(str, datum.get(field)) for datum in local_data if datum.get(field) is not None
    }:
        result_str = ', '.join(sorted(result))
        return fill(result_str, width=70, initial_indent='*  ', subsequent_indent='*  ',
                    break_long_words=False, break_on_hyphens=False)

    # No results:
    return None


def get_industry_cap(industry: str) -> float:
    """Return the sum of all cap values for given industry, use
       the _cap_str_to_mln_float to parse the cap values,
       return a float with 2 digit precision"""
    local_data = _get_data()
    group = [datum for datum in local_data if datum['industry'] == industry]
    result = sum(_cap_str_to_mln_float(datum['cap']) for datum in group)
    return round(result, 2)


def get_stock_symbol_with_highest_cap() -> str:
    """Return the stock symbol (e.g. PACD) with the highest cap, use
       the _cap_str_to_mln_float to parse the cap values"""
    local_data = _get_data()
    result = sorted(local_data, key=lambda e: _cap_str_to_mln_float(e['cap']), reverse=True)[0]
    return result['symbol']


def get_sectors_with_max_and_min_stocks() -> tuple[str, str]:
    """Return a tuple of the sectors with most and least stocks,
       discard n/a"""
    local_data = _get_data()
    #
    # Better:
    # sectors = Counter(
    #     datum['sector'] for datum in local_data if datum['sector'] != 'n/a'
    # ).most_common()
    # return sectors[0][0], sectors[-1][0]
    sectors = Counter(datum['sector'] for datum in local_data).most_common()
    first, last = 0, -1
    while True:
        first_sector = sectors[first][0]
        last_sector = sectors[last][0]

        if first_sector == 'n/a':
            first += 1
        elif last_sector == 'n/a':
            last -= 1
        else:
            break

    return first_sector, last_sector


def testrun() -> None:
    local_data = _get_data()
    pprint(local_data[:3])

    print('\nTesting:')
    industry = 'Advertising'
    print(f'{industry} industry cap:  {get_industry_cap(industry)}')
    print(f'Highest cap:  {get_stock_symbol_with_highest_cap()}')
    print(f'Sectors with min and max stocks:  {get_sectors_with_max_and_min_stocks()}')


def main(*, test: bool=False, verbose: bool=False) -> None:
    # Prime data:
    _get_data(verbose=verbose)

    if test:
        testrun()


# When run as main program:
if __name__ == '__main__':
    main(test=True, verbose=True)

