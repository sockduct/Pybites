#! /usr/bin/env python3.13
'''
After our Code Challenge 62 / Alicante PyDay last week, we thought it would be
nice to branch off a Bite exercise using what we learned. So prepare to do some
web scraping using BeautifulSoup and discover a new library called
gender_guesser. We are going to look at the percentage of female speakers at
Pycon US 2019.

Here is what you need to do:
* Complete get_pycon_speaker_first_names extracting all names from PYCON_HTML we
  cached somewhere for you. Note that some entries have multiple names separated
  by comma (,) and slash (/), so you will need to extract those. Return a list
  of first names.
* Complete get_percentage_of_female_speakers using gender_guesser.detector's
  Detector() to determine the gender based on the first names passed in. This
  tool is not perfect: some names won't be found. However we like Pareto's
  principle so we're happy to get a rough indication. Return the percentage of
  female speakers rounded to 2 decimal places.

If next year's Pycon site doesn't change much, you now have a re-usable script
you can run against Pycon 2020's data...
'''


from urllib.request import urlretrieve
import os
from pathlib import Path
from shutil import copy2

import gender_guesser.detector as gender
from bs4 import BeautifulSoup as Soup

TMP = Path(os.getenv("TMP", "/tmp"))
CWD = Path(__file__).parent
DATA = CWD / 'data'
PYCON_HTML = TMP / "pycon2019.html"
PYCON_PAGE = 'https://bites-data.s3.us-east-2.amazonaws.com/pycon2019.html'

if not PYCON_HTML.exists():
    urlretrieve(PYCON_PAGE, PYCON_HTML)
    if DATA.exists():
        copy2(PYCON_HTML, DATA / PYCON_HTML.name)


def _get_soup(html=PYCON_HTML):
    return Soup(html.read_text(encoding="utf-8"), "html.parser")


def get_pycon_speaker_first_names(soup=None):
    """Parse the PYCON_HTML using BeautifulSoup, extracting all
       speakers (class "speaker"). Note that some items contain
       multiple speakers so you need to extract them.
       Return a list of first names
    """
    pass


def get_percentage_of_female_speakers(first_names):
    """Run gender_guesser on the names returning a percentage
       of female speakers (female and mostly_female),
       rounded to 2 decimal places."""
    pass


if __name__ == '__main__':
    names = get_pycon_speaker_first_names()
    perc = get_percentage_of_female_speakers(names)
    print(perc)
