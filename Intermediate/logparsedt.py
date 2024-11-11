#! /usr/bin/env python3


from datetime import datetime, timedelta
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


def convert_to_datetime(line: str) -> datetime:
    """TODO 1:
       Extract timestamp from logline and convert it to a datetime object.
       For example calling the function with:
       INFO 2014-07-03T23:27:51 supybot Shutdown complete.
       returns:
       datetime(2014, 7, 3, 23, 27, 51)

       Example dt:  2014-07-03T23:31:22
    """
    '''
    Alternative approach:
    timestamp = line.split()[1]
    date_str = '%Y-%m-%dT%H:%M:%S'
    return datetime.strptime(timestamp, date_str)
    '''
    return datetime.strptime(line.split()[1], '%Y-%m-%dT%H:%M:%S')


def time_between_shutdowns(loglines: list[str]) -> timedelta:
    """TODO 2:
       Extract shutdown events ("Shutdown initiated") from loglines and
       calculate the timedelta between the first and last one.
       Return this datetime.timedelta object.
    """
    '''
    Alternative approach:
    shutdown_entries = [line for line in loglines if SHUTDOWN_EVENT in line]
    shutdown_times = [convert_to_datetime(event) for event in shutdown_entries]
    return max(shutdown_times) - min(shutdown_times)  # Nice - independent of temporal ordering!
    '''
    events = [logline for logline in loglines if logline.strip().endswith(f'{SHUTDOWN_EVENT}.')]
    return convert_to_datetime(events[1]) - convert_to_datetime(events[0])


# Must be in module scope for tests:
loglines = get_data()


if __name__ == '__main__':
    print(f'The first logline is:\n{loglines[0]}\nThe extracted datetime object is:\n'
          f'{convert_to_datetime(loglines[0])}')
    print('\nTime between first and last shutdown initiation:\n'
          f'{time_between_shutdowns(loglines).seconds:,.2f} seconds.')
