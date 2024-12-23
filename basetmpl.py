#! /usr/bin/env python3.13


from pathlib import Path
from urllib.request import urlretrieve


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = '<file>'
URL = 'https://bites-data.s3.us-east-2.amazonaws.com'


# Module
def get_data(datafile: str=DATAFILE, datadir: Path=DATADIR, url: str=URL,
             filext: str='.txt', verbose: bool=True) -> None:
    if not datadir.exists():
        datadir.mkdir()

    if not (datafilep := Path(datafile)).suffix:
        datafilep = datafilep.with_suffix(filext)

    data = datadir/datafilep
    if not data.exists():
        if verbose:
            print(f'Retrieving data and saving to {data}.')
        urlretrieve(f'{url}/{datafile}', data)
    elif verbose:
        print(f'{data} already present.')


def do_stuff() -> ...:
    file = DATADIR/DATAFILE if 'DATADIR' in globals() else TEMPFILE
    ...


if __name__ == '__main__':
    get_data()
