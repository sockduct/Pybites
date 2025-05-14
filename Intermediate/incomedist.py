#! /usr/bin/env python3.13
'''
In this Bite you are going to parse some Latin American countries in xml,
specifically the output of api.worldbank.org/V2/country?region=LCN which we
stored here. It's already saved for you in the countries temp file.

Complete get_income_distribution by reading in this file, parsing its XML and
returning a dict of keys = wb:incomeLevel and values = lists of country names
(wb:name). defaultdict is a convenient data structure to use here. See also the
tests for the expected return.

Good luck and code more Python!
'''


from collections import defaultdict
import os
from pathlib import Path
from pprint import pprint
import sys
from urllib.request import urlretrieve
from xml.etree import ElementTree

sys.path.append(str(Path(__file__).resolve().parent.parent))

from basetmpl import get_data, get_path


CWD = Path(__file__).parent
# Where to store retrieved data:
DATADIR = CWD/'data'
# Filename for retrieved data:
DATAFILE = 'countries.xml'
countries = DATADIR/DATAFILE


# import the countries xml file
'''
tmp = Path(os.getenv("TMP", "/tmp"))
countries = tmp / 'countries.xml'

if not countries.exists():
    urlretrieve(
        'https://bites-data.s3.us-east-2.amazonaws.com/countries.xml',
        countries
    )
'''


def get_income_distribution(xml: str|Path=countries) -> defaultdict[str, list[str]]:
    """
    - Read in the countries xml as stored in countries variable.
    - Parse the XML
    - Return a dict of:
      - keys = incomes (wb:incomeLevel)
      - values = list of country names (wb:name)

    Alternative implementation:
    import xml.dom.minidom as md

    dom = md.parse(xml)
    for elem in dom.getElementsByTagName('wb:country'):
        wb_name = elem.getElementsByTagName('wb:name')
        country = wb_name[0].childNodes[0].data

        wb_income = elem.getElementsByTagName('wb:incomeLevel')
        income = wb_income[0].childNodes[0].data
    """
    results: defaultdict[str, list[str]] = defaultdict(list)
    tree = ElementTree.parse(xml)
    root = tree.getroot()
    ns = {'wb': 'http://www.worldbank.org'}
    for country in root.findall('wb:country', ns):
        income_level = country.find('wb:incomeLevel', ns)
        name = country.find('wb:name', ns)
        if income_level is not None and income_level.text and name is not None and name.text:
            results[income_level.text].append(name.text)
        else:
            print(f'Warning:  Skipping record with missing data ({country.attrib=})...')

    return results


if __name__ == '__main__':
    datapath = get_path(datafile=DATAFILE, datadir=DATADIR)
    get_data(datafile=DATAFILE, datapath=datapath, verbose=True)
    pprint(get_income_distribution())
