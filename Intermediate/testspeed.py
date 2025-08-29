#! /usr/bin/env python3.13
'''
In this Bite you will parse a pytest output summary, calculating the Bite that
has the fastest average tests.

Log snippet (full log):
01 =========================== 2 passed in 0.06 seconds ===========================
02 =========================== 6 passed in 0.04 seconds ===========================
03 =========================== 4 passed in 0.74 seconds ===========================
04 =========================== 2 passed in 0.96 seconds ===========================
...

You need to parse out the first number, which is the Bite, the number tests
executed (**only** look at passing tests!), and the seconds it took. Return the Bite
number that had the fastest average runtime per test.

For example:
>>> lines
['01 =========================== 2 passed in 0.06 seconds ===========================',
 '02 =========================== 6 passed in 0.04 seconds ===========================',
 '03 =========================== 4 passed in 0.74 seconds ===========================',
 '04 =========================== 2 passed in 0.96 seconds ===========================']
>>> get_bite_with_fastest_avg_test(lines)
'02'

Which is a clear winner if you do the math:
>>> 0.06/2  # bite 01
0.03
>>> 0.04/6  # bite 02
0.006666666666666667  <== Bite with fastest average
>>> 0.74/4  # bite 03
0.185
>>> 0.96/2  # bite 04
0.48

So a bit of text parsing, calculation and sorting in this Bite. Have fun and
keep calm and code in Python!
'''


import os
from pathlib import Path
import re
from typing import TypedDict
from urllib.request import urlretrieve

tmp = Path(os.getenv("TMP", "/tmp"))
timings_log = tmp / 'pytest_timings.out'
if not timings_log.exists():
    urlretrieve(
        'https://bites-data.s3.us-east-2.amazonaws.com/pytest_timings.out',
        timings_log
    )


class Answer(TypedDict):
    bite: str
    duration: float


def get_bite_with_fastest_avg_test(timings: list[str]) -> str:
    """Return the bite which has the fastest average time per test"""
    answer: Answer = {'bite': '', 'duration': 0.0}
    for line in timings:
        ### Need to work on regex match using online tool:
        match line:
            case c if (
                m := re.match(
                    r'(\d+)\s+=+ (\d+) passed in (\d+\.\d+) seconds =+$', line, re.I
                )
            ):
                bite = m[1]
                duration: float = float(m[3])/int(m[2])
            case c if (
                m := re.match(
                    r'(\d+)\s+=+ (\d+) passed, \d+ warnings in (\d+\.\d+) seconds =+$', line, re.I
                )
            ):
                bite = m[1]
                duration = float(m[3])/int(m[2])
            case c if (
                m := re.match(
                    r'(\d+)\s+=+ \d+ error in (\d+\.\d+) seconds =+$', line, re.I
                )
            ):
                continue
            case c if (
                m := re.match(
                    r'(\d+)\s+=+ no tests ran in (\d+\.\d+) seconds =+$', line, re.I
                )
            ):
                continue
            case _:
                raise ValueError(f'Unable to parse line:  {line}')


        if duration < answer['duration'] or answer['bite'] == '':
            answer['bite'] = bite
            answer['duration'] = duration

    return answer['bite']


if __name__ == '__main__':
    with open(timings_log) as infile:
        data = infile.read().splitlines()
    print(get_bite_with_fastest_avg_test(data))
