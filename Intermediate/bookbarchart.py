#! /usr/bin/env python3.13


import os
from pathlib import Path
import re
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


def create_chart():
    datafile = get_path(datafile=DATA, datadir=DATADIR) if 'DATADIR' in globals() else SAFARI_LOGS
    with open(datafile, encoding='utf8') as infile:
        books = 0
        commands = set()
        for line in infile:
            # Book starting with ISBN-10/ISBN-13 or 032161INTELLEZY or 200000006A0102
            if res := re.search(r'\s+DEBUG\s+\d+\w*\s+-\s+', line):
                books += 1
            # "Command" line:
            elif res := re.search(r'\s+DEBUG\s+-\s+([A-Za-z]+)', line, re.IGNORECASE):
                commands.add(res[1])
            # Parsing error:
            else:
                raise ValueError(f'Unexpected line:  "{line}"')

    print(f'\nBooks:  {books:,}\n'
          f'Commands:  {", ".join(sorted(commands))}\n')


if __name__ == '__main__':
    datapath = get_path(datafile=DATA, datadir=DATADIR)
    get_data(datafile=DATA, datapath=datapath, verbose=True)
    create_chart()
