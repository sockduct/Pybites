#! /usr/bin/env python3.13


from collections import defaultdict
import os
from pathlib import Path
import sys
import urllib.request

sys.path.append(str(Path(__file__).parent.parent))

from basetmpl import get_data, get_path

TMP = os.getenv("TMP", "/tmp")
DATA = 'safari.logs'
SAFARI_LOGS = os.path.join(TMP, DATA)
PY_BOOK, OTHER_BOOK = '🐍', '.'
#
CWD = Path(__file__).parent
DATADIR = CWD/'data'

'''
urllib.request.urlretrieve(
    f'https://bites-data.s3.us-east-2.amazonaws.com/{DATA}',
    SAFARI_LOGS
)
'''


def create_chart() -> None:
    '''
    Example input:
    02-13 01:59 root  DEBUG  9781788838542 - WinOps - DevOps on the Microsoft Azure Stack: VSTS and TFS 2018
    02-13 01:59 root  DEBUG  - sending to slack channel
    02-13 01:59 root  DEBUG  9781787285217 - Python Web Scraping Cookbook
    02-13 01:59 root  DEBUG  - cached, skipping

    Goal:
    * Count the sending to slack channel entries
      * If previous line was Python book print '🐍' else print '.'
    '''
    datafile = get_path(datafile=DATA, datadir=DATADIR) if 'DATADIR' in globals() else SAFARI_LOGS
    with open(datafile, encoding='utf8') as infile:
        output = defaultdict(list)
        for line in infile:
            match line.strip().split():
                case [date, time, 'root', 'DEBUG', idnum, '-', *title]:
                    book_line = dict(date=date, idnum=idnum, title=title)
                case [date, time, 'root', 'DEBUG', '-', 'sending', 'to', 'slack', 'channel']:
                    counter = '🐍' if 'python' in ' '.join(book_line['title']).lower() else '.'
                    output[book_line['date']].append(counter)
                case [date, time, 'root', 'DEBUG', '-', 'cached,', 'skipping']:
                    pass
                case _:
                    raise ValueError(f'Unexpected line:  "{line}"')

        for date, counts in output.items():
            print(f'{date} {"".join(counts)}')


if __name__ == '__main__':
    datapath = get_path(datafile=DATA, datadir=DATADIR)
    get_data(datafile=DATA, datapath=datapath, verbose=False)
    create_chart()
