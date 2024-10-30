#! /usr/bin/env python3


from collections import Counter
import os
from pathlib import Path
from pprint import pprint
import urllib.request
import xml.etree.ElementTree as ET


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'feed.xml'


# Module
def get_data():
    data_loc = DATADIR/DATAFILE

    if not DATADIR.exists():
        DATADIR.mkdir()

    if not data_loc.exists():
        print(f'Retrieving data and saving to {data_loc}.')
        # Retrieve data:
        urllib.request.urlretrieve('https://bites-data.s3.us-east-2.amazonaws.com/feed', data_loc)
    else:
        print(f'{data_loc} already present.')


def get_pybites_top_tags(n=10):
    """use Counter to get the top 10 PyBites tags from the feed
       data already loaded into the content variable"""
    tree = ET.parse(DATADIR/DATAFILE)
    root = tree.getroot()
    return Counter(node.text.lower() for node in root.findall('.//category')).most_common(n)


if __name__ == '__main__':
    get_data()
    '''
    with open(DATADIR/DATAFILE) as infile:
        content = infile.read().lower()
    '''

    res = get_pybites_top_tags()
    pprint(res)
