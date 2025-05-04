#! /usr/bin/env python3.13
'''
Let's get some inspiration. Below you find the simplified HTML of Richard
Branson's My top 10 quotes on living life better
(https://www.virgin.com/richard-branson/my-top-10-quotes-living-life-better).

Parse out the quotes and return a dict where the keys are authors and values
quotes:

>>> from pprint import pprint as pp
>>> from quotes import extract_quotes
>>> pp(extract_quotes())
{'B.B King': 'The beautiful thing about learning is nobody can take it away '
             'from you.',
...
'Zig Ziglar': 'Success means doing the best we can with what we have. Success '
              'is the doing, not the getting; in the trying, not the triumph. '
              'Success is a personal standard, reaching for the highest that '
              'is in us, becoming all that we can be.'}

Good luck and keep calm and code in Python!
'''


from pprint import pprint
import re

from bs4 import BeautifulSoup
import requests


# source: https://www.virgin.com/richard-branson/my-top-10-quotes-living-life-better
ORIGIN = 'https://www.virgin.com/richard-branson/my-top-10-quotes-living-life-better'
HTML = """<!DOCTYPE html>
<head>
  <meta charset="utf-8" />
  <title>My top 10 quotes on living life better | Virgin</title>
</head>
<body>
  <div class="content">
    <p>I’m striving this year to maintain my fitness and to always be learning new things. The new theme on Virgin.com is Live Life Better – a series shining a spotlight on how we can all lead happier, healthier and more fulfilled lives. Virgin has always wanted to make things better for our team and customers and to improve their experiences.</p>
    <p>Here are my top 10 quotes on living life better for some New Year inspiration:</p>
    <p>10. "The beautiful thing about learning is nobody can take it away from you." - B.B King</p>
    <p>9. "Inexperience is an asset. Embrace it." - Wendy Kopp</p>
    <p>8. "Change will not come if we wait for some other person, or if we wait for some other time. We are the ones we’ve been waiting for. We are the change that we seek." - Barack Obama</p>
    <p>7. "The sky is not my limit… I am." - T.F. Hodge</p>
    <p>6. "Life is either a daring adventure or nothing at all." - Helen Keller</p>
    <p>5. "It does not matter how slowly you go as long as you do not stop." - Confucius</p>
    <p>4. "Too many of us are not living our dreams because we are living our fears." - Les Brown</p>
    <p>3. "Continuous efforts – not strength or intelligence – is the key to unlocking our potential." - Winston Churchill</p>
    <p>2. "Believe you can and you’re halfway there." - Theodore Roosevelt</p>
    <p>1. "Success means doing the best we can with what we have. Success is the doing, not the getting; in the trying, not the triumph. Success is a personal standard, reaching for the highest that is in us, becoming all that we can be." - Zig Ziglar</p>
    <p>How do you try and live a healthier, happier life?</p>
  </div>
</body>
</html>"""


def extract_quotes_bs(html: str = HTML) -> dict[str, str]:
    """
    Parse out the quotes and return a dict where the keys are authors and values
    quotes
    """
    soup = BeautifulSoup(html, 'html.parser')
    quote_pattern = re.compile(r'^\d{1,2}\.\s')
    quotes = soup.find_all('p', string=quote_pattern)
    dquote_pattern = r'["“”„‟]'
    dash_pattern = r'[-‐‑‒–—―﹣－]'
    quote_author_pattern = re.compile(
        rf'{dquote_pattern}(.*){dquote_pattern}\s+{dash_pattern}\s+(.*)'
    )
    auth_quotes = {}
    for quote in quotes:
        if result := re.search(quote_author_pattern, quote.text):
            quotation, author = result.groups()
            author = author.replace('\xa0', ' ').strip()
            auth_quotes[author] = quotation

    return auth_quotes


def extract_quotes(html: str = HTML) -> dict[str, str]:
    """
    Parse out the quotes and return a dict where the keys are authors and values
    quotes
    """
    # Alternatively:
    # paras = re.findall('<p>\d+\.(.*?)</p>', html)
    # quotes = {}
    # for p in paras:
    #     quote, author = p.strip().split('-')
    #     quotes[author.strip()] = quote.strip('" ')
    quote_pattern = re.compile(r'<p>\s*\d{1,2}\.\s"(?P<quote>.*)"\s+-\s+(?P<author>.*)\s*</p>')
    return {
        result['author']: result['quote']
        for line in html.splitlines() if (result := re.search(quote_pattern, line))
    }


if __name__ == '__main__':
    print('From embedded static content:')
    pprint(extract_quotes())

    print('\nFrom site:')
    html_doc = requests.get(ORIGIN).text
    pprint(extract_quotes_bs(html_doc))
