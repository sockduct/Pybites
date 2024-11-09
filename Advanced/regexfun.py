#! /usr/bin/env python3


import re


COURSE = ('Introduction 1 Lecture 01:47'
          'The Basics 4 Lectures 32:03'
          'Getting Technical!  4 Lectures 41:51'
          'Challenge 2 Lectures 27:48'
          'Afterword 1 Lecture 05:02')
TWEET = ('New PyBites article: Module of the Week - Requests-cache '
         'for Repeated API Calls - http://pybit.es/requests-cache.html '
         '#python #APIs')
HTML = ('<p>pybites != greedy</p>'
        '<p>not the same can be said REgarding ...</p>')

# References:
LEGAL_URI_SYM = "._~:/?#@!$&'()*+,;=."  # Except brackets ([])
LEGAL_DOM = 'a-zA-Z0-9-'


def extract_course_times(course: str=COURSE) -> list[str]:
    """Return the course timings from the passed in
       course string. Timings are in mm:ss (minutes:seconds)
       format, so taking COURSE above you would extract:
       ['01:47', '32:03', '41:51', '27:48', '05:02']
       Return this list.
    """
    return re.findall(r'\d{2}:\d{2}', course)


def get_all_hashtags_and_links(tweet: str=TWEET) -> list[str]:
    """Get all hashtags and links from the tweet text
       that is passed into this function. So for TWEET
       above you need to extract the following list:
       ['http://pybit.es/requests-cache.html',
        '#python',
        '#APIs']
       Return this list.
    """
    pattern1 = (fr"https?://[{LEGAL_DOM}]+(?:\.[{LEGAL_DOM}]+){{1,}}"
                fr"(?:/[{LEGAL_DOM}{LEGAL_URI_SYM}[\]]*)?")
    pattern2 = r'#[^\W\d_]\w*\b'
    res = []

    res.extend(re.findall(f'(?:{pattern1})|(?:{pattern2})', tweet, re.UNICODE))

    return res


def match_first_paragraph(html: str=HTML) -> str:
    """Extract the first paragraph of the passed in
       html, so for HTML above this would be:
       'pybites != greedy' (= content of first paragraph).
       Return this string.
    """
    pattern = r'<[pP]>(.*?)</[pP]>'
    res = re.search(pattern, html, re.UNICODE)
    return res[1] if res else ''


if __name__ == '__main__':
    print(f'extract_course_times:\n{extract_course_times()}')
    print(f'\nget_all_hashtags_and_links:\n{get_all_hashtags_and_links()}')
    print(f'\nmatch_first_paragraph:\n{match_first_paragraph()}')
