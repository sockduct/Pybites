#! /usr/bin/env python3.13


from pathlib import Path
from urllib.request import urlretrieve


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'UNDEFINED'
URL = 'https://bites-data.s3.us-east-2.amazonaws.com'


# Module
def get_path(datafile: str=DATAFILE, datadir: Path=DATADIR, filext: str='.txt') -> Path:
    '''
    Return full path to datafile (Path object)
    '''
    if datafile == 'UNDEFINED':
        raise ValueError('DATAFILE must be defined with the correct filename.')

    if not datadir.exists():
        datadir.mkdir()

    if not (datafilext := Path(datafile)).suffix:
        datafilext = datafilext.with_suffix(filext)

    return datadir/datafilext


def get_data(datafile: str=DATAFILE, datapath: str|Path|None=None, url: str=URL,
             verbose: bool=False) -> None:
    '''
    Retrieve data from AWS S3 and store in datapath (Path object to datafile)
    '''
    if datafile == 'UNDEFINED':
        raise ValueError('DATAFILE must be defined with the correct filename.')

    if datapath is None:
        datapath = get_path(datafile)
    elif isinstance(datapath, str):
        datapath = Path(datapath)

    if not datapath.exists():
        if verbose:
            print(f'Retrieving data and saving to {datapath}.')
        urlretrieve(f'{url}/{datafile}', datapath)
    elif verbose:
        print(f'{datapath} already present.')


def do_stuff() -> None:
    '''
    Example to differentiate between local and cloud environment:
    file = get_path() if 'DATAFILE' in globals() else TEMPFILE
    '''
    pass


if __name__ == '__main__':
    get_data(verbose=True)
