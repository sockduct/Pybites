#! /usr/bin/env python3.13
'''
The Tim Ferriss Show is full of wisdom and inspiration. It can also quickly fill
up your book shelves because a lot of awesome titles get recommended.

This raises the question: which books to prioritize? We found this list
(https://tim.blog/2017/11/18/booklist/) but for some the Top Books (multiple
mentions) might still be a daunting list!

Luckily we are PyBites Ninjas so what if we use some BeautifulSoup to scrape (a
static copy of) the site to see which books get recommended most.

Complete get_top_books below to find the answer. See the docstring for more info
and again, we don't use the live page, we work with this static copy so we can
reliably test your code. Keep calm and code in Python!
'''


from collections import Counter, defaultdict
from pathlib import Path
from pprint import pprint
import sys

from bs4 import BeautifulSoup
import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))

from basetmpl import get_data, get_path


AMAZON = 'amazon.com'
# static copy
TIM_BLOG = ('https://bites-data.s3.us-east-2.amazonaws.com/tribe-mentors-books.html')
MIN_COUNT = 3
#
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'tribe-mentors-books.html'


def load_page() -> str:
    """Download the blog html and return its decoded content"""
    with requests.Session() as session:
        return session.get(TIM_BLOG).content.decode('utf-8')


def get_top_books(content: str|None=None) -> list[tuple[str, int]]:
    """Make a BeautifulSoup object loading in content,
       find all links that contain AMAZON, extract the book title
       (stripping spacing characters), and count them.
       Return a list of (title, count) tuples where
       count is at least MIN_COUNT
    """
    if content is None:
        content = load_page()

    soup = BeautifulSoup(content, 'html.parser')
    '''
    # Alternative solution:
    books = [link.text.strip() for link in soup.find_all("a")
             if AMAZON in link["href"]]

    return [book for book in Counter(books).most_common()
            if book[1] >= MIN_COUNT]
    '''
    books: defaultdict[str, int] = defaultdict(int)
    for link in soup.find_all('a'):
        if (site := link.get('href')) and AMAZON in site:
            books[link.text.strip()] += 1

    qualified = {book: count for book, count in books.items() if count >= MIN_COUNT}
    return list(sorted(qualified.items(), key=lambda item: item[1], reverse=True))


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=True)

    res = get_top_books(datapath.read_text(encoding='utf8'))
    pprint(res)
