#! /usr/bin/env python3.13
'''
In this Bite we want to figure out how active we've been on our blog.

To start our data analysis we ran the following command on our blog repo:
git log --stat | egrep "^Date|file.*changed," | grep -B1 changed | \\
    grep -v '\\-\\-' | sed 'N;s/\\n/ |/'
which resulted in the following log which should be easier to work with:
Date:   Tue Mar 5 22:34:33 2019 +0100 | 2 files changed, 4 insertions(+), 4 deletions(-)
Date:   Tue Mar 5 20:34:34 2019 +0100 | 1 file changed, 2 insertions(+), 2 deletions(-)
Date:   Tue Mar 5 19:02:56 2019 +0100 | 2 files changed, 31 insertions(+), 2 deletions(-)
Date:   Tue Mar 5 14:18:55 2019 +0100 | 3 files changed, 3 insertions(+), 3 deletions(-)
Date:   Tue Mar 5 14:03:55 2019 +0100 | 2 files changed, 51 insertions(+), 39 deletions(-)
Date:   Tue Mar 5 13:23:51 2019 +0100 | 4 files changed, 109 insertions(+), 94 deletions(-)
...
[930 rows more]
...

Complete get_min_max_amount_of_commits, parsing this file into a dict where keys
are year/months and values are the total number of changes as measured by #
insertions + # deletions (number of file changes can be ignored).

For date parsing you can use the datetime or dateutil module. See the provided
YEAR_MONTH constant for the exact format.

Return a tuple of (least_active_month, most_active_month).

Your code should work if we call it for a smaller data set as well. So if we
pass in the optional year arg of 2018, it should give the min and max month only
for that year (see also the tests).

By the way, with a min, max of ('2019-01', '2019-03'), this year's trend is
looking pretty good so far :)

Good luck and keep calm and code in Python!
'''

from collections import Counter
import os
from pathlib import Path
from pprint import pprint
import re
import sys
from urllib.request import urlretrieve

from dateutil.parser import parse

sys.path.append(str(Path(__file__).resolve().parent.parent))

from basetmpl import get_data, get_path


commits = os.path.join(os.getenv("TMP", "/tmp"), 'commits')
'''
urlretrieve(
    'https://bites-data.s3.us-east-2.amazonaws.com/git_log_stat.out',
    commits
)
'''

# you can use this constant as key to the yyyymm:count dict
YEAR_MONTH = '{y}-{m:02d}'

CWD = Path(__file__).parent
# Where to store retrieved data:
DATADIR = CWD/'data'
REMOTEFILE = 'git_log_stat.out'
# Filename for retrieved data:
LOCALFILE = 'commits.txt'



def get_min_max_amount_of_commits(
    commit_log: str = commits,
    year: int = None
) -> tuple[str, str]:
    """
    Calculate the amount of inserts / deletes per month from the
    provided commit log.

    Takes optional year arg, if provided only look at lines for
    that year, if not, use the entire file.

    Returns a tuple of (least_active_month, most_active_month)
    """
    commits = Counter()
    # Need to account for year filter...
    with open(commit_log, mode='r', encoding='utf8') as infile:
        pattern = (
            r'Date:\s+(\w+ \w+ \d+ \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}) | '
            r'\d+ files? changed, (\d+) insertions?\(\+\), (\d+) deletions?\(-\)'
        )
        for lineno, line in enumerate(infile, 1):
            if not (result := re.match(pattern, line, re.IGNORECASE)):
                raise ValueError(f'Unable to parse line #{lineno}:\n{line}')

            dt, insertions, deletions = parse(result[1]), result[2], result[3]
            commits[YEAR_MONTH.format(y=dt.year, m=dt.month)] += insertions + deletions

    return commits


if __name__ == '__main__':
    datapath = get_path(datafile=LOCALFILE, datadir=DATADIR)
    get_data(datafile=REMOTEFILE, datapath=datapath, verbose=False)

    pprint(get_min_max_amount_of_commits(Path('data')/LOCALFILE))
