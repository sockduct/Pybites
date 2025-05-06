#! /usr/bin/env python3.13
'''
In this Bite we will look at some Bite stats logs (usernames have been
anonymized!):

$ head -5 bite_output_log.txt
bite,user,completed
102,ofancourt1,False
101,ofancourt1,False
29,emilham4,False
9,mfilshin6,False

Load in the data using csv's awesome DictReader storing the result in self.rows
in the constructor (__init__). Next finish the 6 defined @property methods using
the loaded in data. Each property returns a single value. Check out the
docstrings and tests for more info.

Good luck and keep calm and code in Python!
'''


from collections import Counter
from csv import DictReader
import os
from pathlib import Path
import sys
from typing import cast
from urllib.request import urlretrieve

from pydantic import BaseModel, ValidationError

sys.path.append(str(Path(__file__).resolve().parent.parent))

from basetmpl import get_data, get_path


TMP = os.getenv("TMP", "/tmp")
LOGS = 'bite_output_log.txt'
# Added invalid record to test validation:
# LOGS = 'bite_output_log2.txt'
'''
DATA = os.path.join(TMP, LOGS)
S3 = 'https://bites-data.s3.us-east-2.amazonaws.com'
if not os.path.isfile(DATA):
    urlretrieve(f'{S3}/{LOGS}', DATA)
'''
#
CWD = Path(__file__).parent
# Where to store retrieved data:
DATADIR = CWD/'data'
# Filename for retrieved data:
DATAFILE = LOGS
#
DATA = DATADIR/DATAFILE


class Record(BaseModel):
    bite: int
    user: str
    completed: bool


class BiteStats:
    def __init__(self, data: str|Path=DATA, validate: bool=False) -> None:
        self.validated = validate
        with open(data, encoding='utf8') as infile:
            if validate:
                self.rows: list[Record|dict[str, str]] = []
                row: dict[str, str]
                for i, row in enumerate(DictReader(infile), 1):
                    try:
                        self.rows.append(Record(**row))  # type: ignore[arg-type]
                    except ValidationError as err:
                        print(f'❌ Validation failed on row {i}: {row}\n{err}')
            else:
                self.rows = list(DictReader(infile))


    @property
    def number_bites_accessed(self) -> int:
        """Get the number of unique Bites accessed"""
        if self.validated:
            return len({row.bite for row in self.rows})  # type: ignore[union-attr]
        else:
            return len({row['bite'] for row in self.rows})  # type: ignore[index]

    @property
    def number_bites_resolved(self) -> int:
        """Get the number of unique Bites resolved (completed=True)"""
        if self.validated:
            return len({row.bite for row in self.rows if row.completed})  # type: ignore[union-attr]
        else:
            return len(
                {
                    row['bite']  # type: ignore[index]
                    for row in self.rows if row['completed'] == 'True'  # type: ignore[index]
                }
            )

    @property
    def number_users_active(self) -> int:
        """Get the number of unique users in the data set"""
        if self.validated:
            return len({row.user for row in self.rows})  # type: ignore[union-attr]
        else:
            return len({row['user'] for row in self.rows})  # type: ignore[index]

    @property
    def number_users_solving_bites(self) -> int:
        """Get the number of unique users that resolved
           one or more Bites"""
        if self.validated:
            return len({row.user for row in self.rows if row.completed})  # type: ignore[union-attr]
        else:
            return len(
                {
                    row['user']  # type: ignore[index]
                    for row in self.rows if row['completed'] == 'True'  # type: ignore[index]
                }
            )

    @property
    def top_bite_by_number_of_clicks(self) -> str:
        """Get the Bite that got accessed the most
           (= in most rows)"""
        # Extract first tuple, first element (tuple=element, count):
        if self.validated:
            # Because requested return type is str:
            return str(
                Counter(
                    row.bite for row in self.rows  # type: ignore[union-attr]
                ).most_common(1)[0][0]
            )
        else:
            return Counter(
                row['bite'] for row in self.rows  # type: ignore[index]
            ).most_common(1)[0][0]

    @property
    def top_user_by_bites_completed(self) -> str:
        """Get the user that completed the most Bites"""
        # Extract first tuple, first element (tuple=element, count):
        if self.validated:
            return Counter(
                row.user for row in self.rows if row.completed  # type: ignore[union-attr]
            ).most_common(1)[0][0]
        else:
            return Counter(
                row['user']  # type: ignore[index]
                for row in self.rows if row['completed'] == 'True'  # type: ignore[index]
            ).most_common(1)[0][0]


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=False)

    print('Original - unvalidated:')
    bitestats = BiteStats()
    for var in vars(BiteStats):
        if var.startswith('_'):
            continue
        print(f'{var} => {getattr(bitestats, var)}')

    print('\nUpdated - validated:')
    validated_bitestats = BiteStats(validate=True)
    for var in vars(BiteStats):
        if var.startswith('_'):
            continue
        print(f'{var} => {getattr(validated_bitestats, var)}')
