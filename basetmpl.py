#! /usr/bin/env python3


from pathlib import Path


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = ...
DATA = DATADIR/DATAFILE


# Module
def get_data():
    if not DATADIR.exists():
        DATADIR.mkdir()

    if not DATA.exists():
        print(f'Retrieving data and saving to {DATA}.')
        # Retrieve DATA:
        ...
    else:
        print(f'{DATA} already present.')
