#! /usr/bin/env python3


from pathlib import Path
import tempfile


# Global Constants:
CWD = Path(__file__).parent
TMPDIR = tempfile.TemporaryDirectory()
DATA = ...


# Module
def get_data():
    # Throw away:
    ## data_dir = TMPDIR
    # Retain:
    data_dir = CWD/'data'
    data_file = data_dir/DATA

    if not data_dir.exists():
        data_dir.mkdir()

    if not data_file.exists():
        print(f'Retrieving data and saving to {data_file}.')
        # Retrieve data_file:
        ...
    else:
        print(f'{data_file} already present.')
