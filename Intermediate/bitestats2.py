#! /usr/bin/env python3.13
'''
In this Bite you will analyze complexity levels of our first 200 Bites of Py
exercises.

We loaded this CSV file with some stats that look like this:
$ head bite_levels.csv
Bite;Difficulty
Bite 1. Sum n numbers;3.45
Bite 2. Regex Fun;4.89
Bite 3. Word Values;3.97
Bite 4. Top 10 PyBites tags;4.72
Bite 5. Parse a list of names;4.48
Bite 6. PyBites Die Hard;6.8
Bite 7. Parsing dates from logs;5.76
Bite 8. Rotate string characters;3.5
Bite 9. Palindromes;4.71
...
...
Bite 200. 🥳 Minecraft Enchantable Items;None

The last column shows the average complexity score if available, if not it shows
None.

Complete the get_most_complex_bites function below following its docstring.

Your code will be tested calling your function with different arguments.

Update: some folks reported hitting a UTF-8 BOM error. In that case use
encoding="utf-8-sig" when opening the csv file.
'''


import csv
import heapq
import os
from pathlib import Path
from pprint import pprint
import re
from urllib.request import urlretrieve


data = 'https://bites-data.s3.us-east-2.amazonaws.com/bite_levels.csv'
TMP = Path(os.getenv("TMP", "/tmp"))
stats = TMP / 'bites.csv'


if not stats.exists():
    urlretrieve(data, stats)


def add_bite(row: dict[str, str]) -> dict[str, str]:
    res = re.match(r'\s*bite\s+(\d{1,3})', row['Bite'], re.I)
    if not res:
        raise ValueError(f'Unexpected bite description:  {row['Bite']}')

    row['Number'] = res[1]

    return row


def is_float(n: int|float|str) -> bool:
    if isinstance(n, str):
        n = n.strip()

    try:
        float(n)
        return True
    except ValueError:
        return False


def get_most_complex_bites(N: int=10, stats: Path=stats, *, verbose: bool=False
                           ) -> list[dict[str, str]]|list[str]:
    """Parse the bites.csv file (= stats variable passed in), see example
       output in the Bite description.
       Return a list of Bite IDs (int or str values are fine) of the N
       most complex Bites.
    """
    with open(stats, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        '''
        # Alternative solution:
        # skip header
        next(reader)
        ret = sorted(reader,
                     key=lambda row: row[1] != 'None' and float(row[1]),
                     reverse=True)
        return [re.sub('Bite (\\d+).*', r'\1', row[0]) for row in ret[:N]]
        '''
        # Only include bites with difficulty rating:
        # data = [add_bite(row) for row in reader if is_float(row['Difficulty'])]
        candidates = heapq.nlargest(
            N, reader, key=lambda row: row['Difficulty'] != 'None' and float(row['Difficulty'])
        )

    # candidates = heapq.nlargest(N, data, key=lambda i: i['Difficulty'])

    return candidates if verbose else [
        re.sub(r'\s*bite\s+(\d{1,3})\..*', r'\1', row['Bite'], flags=re.I) for row in candidates
    ]


if __name__ == '__main__':
    res = get_most_complex_bites(verbose=True)
    pprint(res, width=132)
    pprint(get_most_complex_bites(), width=132)
