import json
import os
from pathlib import Path
import sys
from unittest.mock import patch
from urllib.request import urlretrieve

sys.path.append(str(Path(__file__).resolve().parent.parent))

from nytbest import get_best_seller_titles, URL_NON_FICTION, URL_FICTION

TMP = Path(os.getenv("TMP", "/tmp"))

FICTION = TMP / 'nyt-fiction.json'
if not FICTION.exists():
    urlretrieve(
        'https://bites-data.s3.us-east-2.amazonaws.com/nyt-fiction.json',
        FICTION
    )

NON_FICTION = TMP / 'nyt-nonfiction.json'
if not NON_FICTION.exists():
    urlretrieve(
        'https://bites-data.s3.us-east-2.amazonaws.com/nyt-nonfiction.json',
        NON_FICTION
    )


def mocked_requests_get(*args, **kwargs):
    """https://stackoverflow.com/a/28507806"""

    class MockResponse:

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.ok = True

        def json(self):
            return self.json_data

        def raise_for_status(self):
            pass

    url = args[0]
    fname = NON_FICTION if 'nonfiction' in url else FICTION
    with open(fname) as f:
        return MockResponse(json.loads(f.read()), 200)

    return MockResponse(None, 404)


@patch('requests.get', side_effect=mocked_requests_get)
def test_response_nonfiction(mock_get):
    assert get_best_seller_titles(url=URL_NON_FICTION) == [
        ('BETWEEN THE WORLD AND ME', 86),
        ('EDUCATED', 79),
        ('BECOMING', 41),
        ('THE SECOND MOUNTAIN', 18),
        ('THE PIONEERS', 16),
        ('MAYBE YOU SHOULD TALK TO SOMEONE', 14),
        ('UNFREEDOM OF THE PRESS', 14),
        ('RANGE', 9),
        ('THREE WOMEN', 7),
        ('TRICK MIRROR', 3),
        ('HOW TO BE AN ANTIRACIST', 2),
        ('KOCHLAND', 2),
        ('THANK YOU FOR MY SERVICE', 1),
        ('THE OUTLAW OCEAN', 1),
        ('GODS OF THE UPPER AIR', 1)
    ]


@patch('requests.get', side_effect=mocked_requests_get)
def test_response_fiction(mock_get):
    assert get_best_seller_titles(url=URL_FICTION) == [
        ('WHERE THE CRAWDADS SING', 51),
        ('THE SILENT PATIENT', 25),
        ('EVVIE DRAKE STARTS OVER', 7),
        ('THE NICKEL BOYS', 6),
        ('ASK AGAIN, YES', 6),
        ('ONE GOOD DEED', 5),
        ('THE INN', 3),
        ('THE TURN OF THE KEY', 3),
        ('OUTFOX', 3),
        ('THE BITTERROOTS', 2),
        ('INLAND', 2),
        ('OLD BONES', 1),
        ('THE LAST WIDOW', 1),
        ('THE WHISPER MAN', 1),
        ('TIDELANDS', 1)
    ]
