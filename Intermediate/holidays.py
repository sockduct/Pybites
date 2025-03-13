#! /usr/bin/env python3.13
'''
Parse US holidays from HTML data with BeautifulSoup:
* Check the HTML (S3 bucket data) for a table with CSS class list-table and
  parse its data
* You need to populate the given holidays defaultdict like this:
  >>> from pprint import pprint as pp
  >>> from holidays import get_us_bank_holidays
  >>> pp(get_us_bank_holidays())
  defaultdict(<class 'list'>,
              {'01': ["New Year's Day", 'Martin Luther King Jr. Day'],
               '02': ["Presidents' Day"],
               '04': ['Emancipation Day'],
               '05': ["Mother's Day", 'Memorial Day'],
               '06': ["Father's Day"],
               '07': ['Independence Day'],
               '09': ['Labor Day'],
               '10': ['Columbus Day'],
               '11': ['Veterans Day', 'Thanksgiving', 'Day after Thanksgiving'],
               '12': ['Christmas Day']})
'''



from collections import defaultdict
from pathlib import Path
from pprint import pprint
import sys

from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))

from basetmpl import get_data, get_path


CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'us_holidays.html'


def get_us_bank_holidays(content: str) -> defaultdict[str, list[str]]:
    """Receive scraped html output, make a BS object, parse the bank
       holiday table (css class = list-table), and return a dict of
       keys -> months and values -> list of bank holidays"""
    holidays = defaultdict(list)
    soup = BeautifulSoup(content, 'html.parser')

    # Parse out:
    # * Month - table.tbody.td.time.string
    # * Holiday description - table.tbody.td.a.string
    if soup.table and soup.table.tbody and soup.table.tbody.td:
        for cell in soup.table.tbody.find_all('td'):
            if cell.time:
                month = str(cell.time.string.split('-')[1]).strip()
            elif cell.a:
                holidays[month].append(str(cell.a.string).strip())

    return holidays


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=True)

    content = datapath.read_text()
    pprint(get_us_bank_holidays(content))
