#! /usr/bin/env python3.13
'''
This is a Pandas proof-of-concept Bite. We just added the library to our
platform!

For this Bite you find out the male and female athletes who won most medals in
all the Summer Olympic Games (csv = 1896-2012, but we also test a smaller subset
of the data).
'''


from collections import Counter
from pathlib import Path
import sys

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))

from basetmpl import get_data, get_path


CWD = Path(__file__).parent
# Where to store retrieved data:
DATADIR = CWD/'data'
# Filename for retrieved data:
DATAFILE = 'summer.csv'
# For compatibility with bite:
data = ''


def athletes_most_medals(data: str=data) -> pd.Series:
    if not data:
        data = get_path(datafile=DATAFILE, datadir=DATADIR)

    df = pd.read_csv(data, na_filter=False)
    man = df.loc[df['Gender'] == 'Men', 'Athlete'].value_counts().head(1)
    woman = df.loc[df['Gender'] == 'Women', 'Athlete'].value_counts().head(1)

    return pd.concat([man, woman])


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=False)

    print(athletes_most_medals())
