from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from decowarg import make_html


def test_make_html():
    @make_html('p')
    @make_html('strong')
    def get_text(text='I code with PyBites'):
        return text

    assert get_text() == '<p><strong>I code with PyBites</strong></p>'
