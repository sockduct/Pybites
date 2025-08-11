#! /usr/bin/env python3.13
'''
There is a new Python news aggregator in town: news.python.sc (update April
2023: this site is no longer online, but don't worry, we use a static copy for
this exercise).

Imagine you want to email yourself and colleagues a Friday digest of top
articles, based on number of points and comments.

Our first go would be feedparser but there is not an RSS feed yet.

So in this Bite you will use some BeautifulSoup (4.7.1) to parse the HTML
yourself. Not a bad skill to have, no?

We have you parse a static copy of the site so we have predictable data to test
your code against. As you can see in the tests your code should work with the
second (paginated) page as well.

Note we had some issues getting lxml to work on the platform so use bs4's
html.parser for now. Also the W3C validator does not really like the HTML so you
cannot rely on article or table while parsing out the entries. Search for the
title class instead.

Good luck and bookmark this site to keep up2date with Python news. If you see
anything interesting feel free to share it in our community.

Update 20th of Oct 2019: there is an RSS feed available now, but no count of
comments/points so you will still need BeautifulSoup / scraping. No worries
though, if you want to scrape RSS feeds, take one of our feedparser Bites...

Keep calm and code more Python!
'''


# from collections import namedtuple
from pprint import pformat
from typing import NamedTuple

from bs4 import BeautifulSoup
import requests

# feed = https://news.python.sc/, to get predictable results we cached
# first two pages - use these:
# https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index.html
# https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index2.html

# Entry = namedtuple('Entry', 'title points comments')
class Entry(NamedTuple):
    title: str
    points: int
    comments: int


def _create_soup_obj(url: str) -> BeautifulSoup:
    """Need utf-8 to properly parse emojis"""
    resp = requests.get(url)
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def get_top_titles(url: str, top: int=5) -> list[Entry]:
    """Parse the titles (class 'title') using the soup object.
       Return a list of top (default = 5) titles ordered descending
       by number of points and comments.

       Alternative solution:
       ret = []
       for title in soup.find_all('span', {'class': 'title'}):
           votes_and_comments = title.find_next('td').text
           title = title.text.strip()
           m = re.search('(\\d+) points?.*(\\d+) comments?', votes_and_comments, re.DOTALL)
           points, comments = m.groups()
           ret.append(Entry(title, int(points), int(comments)))

       return sorted(ret, key=itemgetter(1, 2), reverse=True)[:top]
    """
    soup = _create_soup_obj(url)

    entries = []
    title = 'Unknown'
    for element in soup.select('span.title, span.controls'):
        match element.get('class'):
            case ['title']:
                title = element.text.strip()
            case ['controls']:
                data = element.select('span.smaller')[0].text
                points, comments = data.split('|')
                points_int = int(points.strip().split()[0])
                comments_int = int(comments.strip().split()[0])

                entries.append(Entry(title, points_int, comments_int))
                title = 'Unknown'
            case _:
                continue

    return sorted(entries, key=lambda e: e.points + e.comments, reverse=True)[:top]


if __name__ == '__main__':
    url1 = 'https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index.html'
    url2 = 'https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index2.html'
    for url in (url1, url2):
        print(f'get_top_titles({url}):\n{pformat(get_top_titles(url), width=132)}\n')
