#! /usr/bin/env python3.13
'''
In this Bite you parse a copy of StackOverflow Python questions
(https://stackoverflow.com/questions/tagged/python?sort=frequent&pageSize=15)
which we cached here
(https://bites-data.s3.us-east-2.amazonaws.com/so_python.html).

Retrieve + parse this URL with requests + BeautifulSoup and extract the question
(question-hyperlink class), votes (vote-count-post class) and number of views
(views class) into a list.

Next filter the list to only show questions with more than one million views
(HTML = "..m views") and sort the remaining questions descending on number of
votes. See the tests for the expected return output. Some pretty good questions
in that list!

Enjoy and code more Python!
'''


from pathlib import Path
from pprint import pprint
import sys

import requests
try:
    import requests_cache
except ImportError:
    requests_cache = None
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))


cached_so_url = 'https://bites-data.s3.us-east-2.amazonaws.com/so_python.html'


def top_python_questions(url: str=cached_so_url) -> list[tuple[str, int]]:
    """Use requests to retrieve the url / html,
       parse the questions out of the html with BeautifulSoup,
       filter them by >= 1m views ("..m views").
       Return a list of (question, num_votes) tuples ordered
       by num_votes descending (see tests for expected output).
    """
    if requests_cache:
        requests_cache.install_cache('pybites-s3-cache')
    html_doc = requests.get(cached_so_url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    # question-hyperlink class:
    for a_tag in soup.find_all('a', 'question-hyperlink'):
        # Need to navigate up to find votes
        # Extract question ID from href and match it against this:
        # <div class="question-summary" id="question-summary-15112125">
        ...
    '''
    # votes (vote-count-post class)
    for span_tag in soup.find_all('span', 'vote-count-post'):
        ...
    # number of views # (views class)
    for div_tag in soup.find_all('div', 'views'):
        ...
    '''
    # into a list


if __name__ == '__main__':
    pprint(top_python_questions())
