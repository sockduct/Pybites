#! /usr/bin/env python3


from datetime import datetime
from pathlib import Path
import urllib.request


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'messages.log'
DATA = DATADIR/DATAFILE

SHUTDOWN_EVENT = 'Shutdown initiated'


# Module
def get_data() -> list[str]:
    if not DATADIR.exists():
        DATADIR.mkdir()

    if not DATA.exists():
        print(f'Retrieving data and saving to {DATA}.')
        # Retrieve DATA:
        urllib.request.urlretrieve(
            'https://bites-data.s3.us-east-2.amazonaws.com/messages.log',
            DATA
        )
    else:
        print(f'{DATA} already present.')

    with open(DATA) as infile:
        loglines = infile.readlines()

    return loglines


def convert_to_datetime(line):
    """TODO 1:
       Extract timestamp from logline and convert it to a datetime object.
       For example calling the function with:
       INFO 2014-07-03T23:27:51 supybot Shutdown complete.
       returns:
       datetime(2014, 7, 3, 23, 27, 51)

       Example dt:  2014-07-03T23:31:22
    """
    return datetime.strptime(line.split()[1], '%Y-%m-%dT%H:%M:%S')


def time_between_shutdowns(loglines):
    """TODO 2:
       Extract shutdown events ("Shutdown initiated") from loglines and
       calculate the timedelta between the first and last one.
       Return this datetime.timedelta object.
    """
    pass


if __name__ == '__main__':
    loglines = get_data()
