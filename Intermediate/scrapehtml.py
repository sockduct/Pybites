#! /usr/bin/env python3.13


from collections import namedtuple
from pathlib import Path
import sys

from bs4 import BeautifulSoup as Soup
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
    * Populate and return a Book namedtuple
    """
    pass

if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=False)
