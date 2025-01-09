#! /usr/bin/env python3.13


from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from basetmpl import get_data, get_path


CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'UNDEFINED'


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=False)
