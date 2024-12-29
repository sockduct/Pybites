#! /usr/bin/env python3.13


from datetime import timedelta
from pathlib import Path
import re
from urllib.request import urlretrieve


# Global Constants:
CWD = Path(__file__).parent
DATADIR = CWD/'data'
DATAFILE = 'course_timings'
URL = 'https://bites-data.s3.us-east-2.amazonaws.com'


# Module
def get_path(datafile: str=DATAFILE, datadir: Path=DATADIR, filext: str='.txt') -> Path:
    if not datadir.exists():
        datadir.mkdir()

    if not (datafilep := Path(datafile)).suffix:
        datafilep = datafilep.with_suffix(filext)

    return datadir/datafilep


def get_data(datafile: str=DATAFILE, url: str=URL, verbose: bool=False) -> None:
    data_path = get_path()
    if not data_path.exists():
        if verbose:
            print(f'Retrieving data and saving to {data_path}.')
        urlretrieve(f'{url}/{datafile}', data_path)
    elif verbose:
        print(f'{data_path} already present.')


def get_all_timestamps(datafile: Path=get_path()) -> list[str]:
    """Read in the COURSE_TIMES and extract all MM:SS timestamps.
       Here is a snippet of the input file:

       Start  What is Practical JavaScript? (3:47)
       Start  The voice in your ear (4:41)
       Start  Is this course right for you? (1:21)
       ...

        Return a list of MM:SS timestamps
    """
    # course_time_pattern = r'Start\s+[^(]*\((\d{1,2}:\d{2})\)'
    # Simplify - as simple as possible but no simpler:
    course_time_pattern = r'\d{1,2}:\d{2}'
    with open(datafile) as infile:
        return re.findall(course_time_pattern, infile.read())


def parse_mmss(timestamp: str) -> timedelta:
    minutes, seconds = timestamp.split(':')
    return timedelta(minutes=int(minutes), seconds=int(seconds))


def calc_total_course_duration(timestamps: list[str]) -> str:
    """Takes timestamps list as returned by get_all_timestamps
       and calculates the total duration as HH:MM:SS"""
    # Make sure to review __str__ format before creating your own!
    return str(
        sum((parse_mmss(timestamp) for timestamp in timestamps), start=timedelta(seconds=0))
    )


if __name__ == '__main__':
    get_data(verbose=True)
    timestamps = get_all_timestamps()
    print(calc_total_course_duration(timestamps))
