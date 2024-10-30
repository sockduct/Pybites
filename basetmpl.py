#! /usr/bin/env python3


from pathlib import Path


# Global Constants:
CWD = Path(__file__).parent
DATADIR = 'data'
DATAFILE = ...


# Module
def get_data():
    # Retain:
    DATA = DATADIR/DATAFILE

    if not DATADIR.exists():
        DATADIR.mkdir()

    if not DATA.exists():
        print(f'Retrieving data and saving to {DATA}.')
        # Retrieve DATA:
        ...
    else:
        print(f'{DATA} already present.')
