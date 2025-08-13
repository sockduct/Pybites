#! /usr/bin/env python3.13
'''
In this Bite we are going to convert some Warcraft Mount JSON data to csv.

Here are the steps to take:
Complete convert_to_csv that receives a json_file, the files used for this Bite
are hosted here (1), here (2) and here (3) - basically small subsets of the linked gist
above.

(1) https://bites-data.s3.us-east-2.amazonaws.com/mount-data1.json
(2) https://bites-data.s3.us-east-2.amazonaws.com/mount-data2.json
(3) https://bites-data.s3.us-east-2.amazonaws.com/mount-data3.json

Load the JSON into a dict, look for mounts > collected.

If invalid JSON (yes, real developer life!), print "exception caught" (defined
in the EXCEPTION constant) and reraise the exception.

If good data write it to a csv file in /tmp, for example:
$ cat /tmp/mount1.csv
creatureId,icon,isAquatic,isFlying,isGround,isJumping,itemId,name,qualityId,spellId
32158,ability_mount_drake_blue,False,True,True,False,44178,Albino Drake,4,60025
63502,ability_mount_hordescorpionamber,True,False,True,True,85262,Amber Scorpion,4,123886
24487,ability_mount_warhippogryph,False,True,True,False,45725,Argent Hippogryph,4,232412

By the way, yes, you can do this with pandas but for this Bite we are assuming
you don't have access to this library. It's good to learn the standard library!
'''


import csv
import json
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from pprint import pprint, pformat

import requests


EXCEPTION = 'exception caught'
TMP = Path(os.getenv("TMP", "/tmp"))


def convert_to_csv(json_file: Path) -> None:
    """Read/load the json_file (local file downloaded to /tmp) and
       convert/write it to defined csv_file.
        The data is in mounts > collected

       Catch bad JSON (JSONDecodeError) file content, in that case print the defined
       EXCEPTION string ('exception caught') to stdout reraising the exception.
       This is to make sure you actually caught this exception.

       Example csv output:
       creatureId,icon,isAquatic,isFlying,isGround,isJumping,itemId,name,qualityId,spellId
       32158,ability_mount_drake_blue,False,True,True,False,44178,Albino Drake,4,60025
       63502,ability_mount_hordescorpionamber,True,...
       ...
    """  # noqa E501
    csv_file = TMP / json_file.name.replace('.json', '.csv')

    with open(TMP/json_file, encoding='utf8') as infile:
        data = json.load(infile)

    with open(csv_file, mode='w', newline='', encoding='utf8') as outfile:
        fieldnames = data['mounts']['collected'][0].keys()
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for items in data['mounts']['collected']:
            writer.writerow(items)


def main(verbose: bool=False) -> None:
    s3_bucket = 'https://bites-data.s3.us-east-2.amazonaws.com/mount-data{}.json'
    for file in range(1, 4):
        target_file = TMP/s3_bucket.format(file).split('/')[-1]
        with open(target_file, 'w', encoding='utf8') as outfile:
            resp = requests.get(s3_bucket.format(file))

            # Debugging:
            if verbose:
                for i, line in enumerate(pformat(resp.text).splitlines()):
                    print(f'{i:2} {line}')

            try:
                data = resp.json()
            except JSONDecodeError as err:
                print(f'Error decoding data as JSON:\n{err}')
                continue

            json.dump(data, outfile)

        print(f'Invoked {convert_to_csv(target_file)=} with file #{file}...\n')

        if verbose:
            csv_file = TMP / target_file.name.replace('.json', '.csv')

            print(f'{csv_file}:')
            with open(csv_file, encoding='utf8') as infile:
                reader = csv.DictReader(infile)
                for row in reader:
                    print(row)

            print('\nReading file as a list instead of a dict:')
            with open(csv_file, encoding='utf8') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    print(row)

            print('\nRaw file:')
            with open(csv_file, encoding='utf8') as infile:
                for row in infile:
                    print(row)

            print()


if __name__ == '__main__':
    main(verbose=True)
