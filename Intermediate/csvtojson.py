#! /usr/bin/env python3.13
'''
At the 1 year mark of our platform here is Bite 150! In this Bite you are
presented with some messed up csv (to avoid file IO we pre-loaded it into a
multi-line string variable members). The first line is the header and can be
assumed to only have commas, the 10 data rows though have a mix of ",", "|" and
";" delimiters.

But no worries, you Python ninjas can do data cleaning for breakfast no?!

Complete convert_to_json parsing this output and returning valid json like this:

[{"id": "1", "first_name": "Junie", "last_name": "Kybert", "email": "jkybert0@army.mil"},
 {"id": "2", "first_name": "Sid", "last_name": "Churching", "email": "schurching1@tumblr.com"},
 {"id": "3", "first_name": "Cherry", "last_name": "Dudbridge", "email": "cdudbridge2@nifty.com"},
 ... more entries ...
]

The tests will check if your output is indeed valid json and of course if it
contains all data. Good luck!
'''


import json
from pprint import pprint
import re


members = """
id,first_name,last_name,email
1,Junie,Kybert;jkybert0@army.mil
2,Sid,Churching|schurching1@tumblr.com
3,Cherry;Dudbridge,cdudbridge2@nifty.com
4,Merrilee,Kleiser;mkleiser3@reference.com
5,Umeko,Cray;ucray4@foxnews.com
6,Jenifer,Dale|jdale@hubpages.com
7,Deeanne;Gabbett,dgabbett6@ucoz.com
8,Hymie,Valentin;hvalentin7@blogs.com
9,Alphonso,Berwick|aberwick8@symantec.com
10,Wyn;Serginson,wserginson9@naver.com
"""


def _split(line: str) -> list[str]:
    # return re.split(r',|\||;', line)
    # Better:
    return re.split(r'[,|;]', line)


def convert_to_json(members: str=members) -> str:
    result = []
    # for lineno, line in enumerate(members.strip().split('\n')):
    # Better:
    for lineno, line in enumerate(members.strip().splitlines()):
        if lineno == 0:
            keys = _split(line)
        else:
            result.append(dict(zip(keys, _split(line))))

    return json.dumps(result)


if __name__ == '__main__':
    pprint(convert_to_json())
