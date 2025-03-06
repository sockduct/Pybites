#! /usr/bin/env python3.13
'''
Example output:
 {'Agent 1': Counter({'8': 48, '2': 1}),
...
# Counter k,v here = (episode, # number of words spoken)
...
               'Anthropologist': Counter({'12': 101}),
...
               'Cartman': Counter({'1': 735,
                                   '10': 669,
                                   '13': 621,
... etc ...
'''


from collections import Counter, defaultdict
import csv
from io import StringIO
from pprint import pprint

import requests
import requests_cache


CSV_URL = 'https://raw.githubusercontent.com/pybites/SouthParkData/master/by-season/Season-{}.csv' # noqa E501


def get_season_csv_file(season: int) -> str:
    """Receives a season int, and downloads loads in its
       corresponding CSV_URL"""
    # with requests.Session() as s:
    with requests_cache.CachedSession('bite_cache') as s:
        download = s.get(CSV_URL.format(season))
        return download.content.decode('utf-8')


def get_num_words_spoken_by_character_per_episode(content: str):
    """Receives loaded csv content (str) and returns a dict of
       keys=characters and values=Counter object,
       which is a mapping of episode=>words spoken"""
    data = defaultdict(Counter)
    reader = csv.DictReader(StringIO(content, newline=''))
    for row in reader:
        data[row['Character']] += Counter({row['Episode']: len(row['Line'].split())})

    return data


if __name__ == '__main__':
    content = get_season_csv_file(1)
    pprint(get_num_words_spoken_by_character_per_episode(content))
    # print(get_num_words_spoken_by_character_per_episode(content))
