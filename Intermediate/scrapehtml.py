#! /usr/bin/env python3.13


from collections import namedtuple
from pathlib import Path
import re
import sys

from bs4 import BeautifulSoup as Soup
from bs4.element import Tag
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


def get_book() -> Book:
    """
    Goals:
    * Make a Soup object
    * Parse out the relevant fields as defined in Book (from the relevant html sections)
      * Mastering  Typescript - Second Edition
    * Populate and return a Book namedtuple
    """
    # soup = Soup(CONTENT, 'lxml')
    soup = Soup(CONTENT, 'html.parser')
    # Wrong title!
    # title = str(soup.title.string) if soup.title else 'No title found'
    #
    # There's a better way:
    # title = str(
    #   soup.find_all(string=re.compile(r'mastering\s+typescript', re.IGNORECASE))[0].strip()
    # )
    book_section = soup.find('div', 'dotd-main-book-summary')
    '''
    Alternate solution:
    book_image = soup.find('div', {'class': 'dotd-main-book-image'})
    link = book_image.find('a').get('href')
    image = book_image.find('img').get('src')
    book_main = soup.find('div', {'class': 'dotd-main-book-summary'})
    title_div = book_main.find('div', {'class': 'dotd-title'})
    title = title_div.find('h2').text.strip()
    descr_div = title_div.find_next_sibling("div")
    description = descr_div.text.strip()
    '''
    if isinstance(book_section, Tag):
        for line in book_section.contents:
            if isinstance(line, Tag) and (text := ''.join(line.strings).strip()):
                if re.search(r'mastering\s+typescript', text, re.IGNORECASE):
                    title = text
                elif re.search(r'time is running out', text, re.IGNORECASE):
                    continue
                elif '\n' in text:
                    description_details = text
                else:
                    description = text
    else:
        title = None
        description_details = None
        description = None

    if book_section := soup.find('div', 'dotd-main-book-image'):
        if (hyperlink := book_section.find('a')) and isinstance(hyperlink, Tag):
            link = hyperlink['href']
        else:
            link = None
        if (image_tag := book_section.find('img')) and isinstance(image_tag, Tag):
            image = image_tag['src']
        else:
            image = None
    else:
        link = None
        image = None

    return Book(title=title, description=description, image=image, link=link)


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=False)
    book = get_book()
    print(book)
