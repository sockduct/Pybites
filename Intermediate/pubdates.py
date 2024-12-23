#! /usr/bin/env python3.13

from collections import Counter
from datetime import datetime
import os
from pathlib import Path
import re
from urllib.request import urlretrieve


# Included Constants:
BASE_URL = 'https://bites-data.s3.us-east-2.amazonaws.com/'
RSS_FEED = 'pybites_feed.rss.xml'
PUB_DATE = re.compile(r'<pubDate>(.*?)</pubDate>')
TMP = os.getenv("TMP", "/tmp")

# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = RSS_FEED

# String off trailing '/':
URL = BASE_URL[:-1]


# Module
def get_data(datafile: str=DATAFILE, datadir: Path=DATADIR, url: str=URL,
             filext: str='.txt', verbose: bool=True) -> None:
    if not datadir.exists():
        datadir.mkdir()

    if not (datafilep := Path(datafile)).suffix:
        datafilep = datafilep.with_suffix(filext)

    data = datadir/datafilep
    if not data.exists():
        if verbose:
            print(f'Retrieving data and saving to {data}.')
        urlretrieve(f'{url}/{datafile}', data)
    elif verbose:
        print(f'{data} already present.')


def _get_dates() -> list[str]:
    """Downloads PyBites feed and parses out all pub dates returning
       a list of date strings, e.g.: ['Sun, 07 Jan 2018 12:00:00 +0100',
       'Sun, 07 Jan 2018 11:00:00 +0100', ... ]"""
    remote = os.path.join(BASE_URL, RSS_FEED)
    local = os.path.join(TMP, RSS_FEED)
    urlretrieve(remote, local)

    with open(local) as f:
        return PUB_DATE.findall(f.read())


def convert_to_datetime(date_str: str, tz: bool=False) -> datetime:
    """
    Receives a date str and convert it into a datetime object

    Format:
    Thu, 04 May 2017 20:46:00 +0200

    Note:  Don't have to deal with time zone.
    """
    if tz:
        dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    else:
        date_str = date_str[-6]
        dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S')


def get_month_most_posts(dates: list[str]) -> str:
    """Receives a list of datetimes and returns the month (format YYYY-MM)
       that occurs most"""
    dt_list = [convert_to_datetime(date) for date in dates]
    return Counter(dt.strftime('%Y-%d') for dt in dt_list).most_common(1)


if __name__ == '__main__':
    get_data()
    date_data = _get_dates()
    print(get_month_most_posts(date_data))
