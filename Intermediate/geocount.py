#! /usr/bin/env python3.13


from collections import Counter
import csv

import requests


CSV_URL = 'https://bites-data.s3.us-east-2.amazonaws.com/community.csv'
TIMEOUT = 5


def get_csv(url: str=CSV_URL) -> str:
    """Use requests to download the csv and return the
       decoded content"""
    resp = requests.get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.text


def create_user_bar_chart(content: str) -> None:
    """Receives csv file (decoded) content and print a table of timezones
       and their corresponding member counts in pluses to standard output
    """
    counts = Counter(line['tz'] for line in csv.DictReader(content.splitlines()))
    colsize = max(map(len, counts))
    for item, val in sorted(counts.items()):
        print(f'{item:<{colsize}} | {"+" * val}')

if __name__ == '__main__':
    data = get_csv()
    create_user_bar_chart(data)
