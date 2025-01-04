#! /usr/bin/env python3.13


from collections import namedtuple
from pathlib import Path
from re import compile, IGNORECASE as ignorecase
import sys

from bs4 import BeautifulSoup as Soup
import bs4
import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))
from basetmpl import get_data, get_path


PACKT = 'https://bites-data.s3.us-east-2.amazonaws.com/packt.html'
CONTENT = requests.get(PACKT).text
#
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'packt.html'


Book = namedtuple('Book', 'title description image link')


def get_book():
    """
    Goals:
    * Make a Soup object
    * Parse out the relevant fields as defined in Book (from the relevant html sections)
      * Mastering  Typescript - Second Edition
    * Populate and return a Book namedtuple
    """
    soup = Soup(CONTENT, 'lxml')
    # title = str(soup.title.string) if soup.title else 'No title found'
    title = str(soup.find_all(string=compile(r'mastering\s+typescript', ignorecase))[0].strip())
    descr_section = soup.find_all('div', 'dotd-main-book-summary')[0]
    for n, line in enumerate(descr_section.contents):
        if isinstance(line, bs4.element.Tag) and (res := ''.join(line.strings).strip()):
            print(f'({n}) {type(line)}:  {res}')

if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=False)
    book = get_book()
    print(book)
