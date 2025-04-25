#! /usr/bin/env python3.13
'''
Another unicode Bite. Given some non-English text with accents (á, é, í, used in
Spanish for example), extract the accented characters. That's it.

Check out the unicodedata module which should make this fairly straightforward.

Another unicode Bite you can take is: Emoji (Unicode).
Additional article resource: How Encoding Works in Python

Have fun and if you have ideas for more unicode Bites, let us know ...
'''


from unicodedata import decomposition


def filter_accents(text: str) -> list[str]:
    """Return a sequence of accented characters found in
       the passed in lowercased text string
    """
    return [char for char in text.lower() if decomposition(char)]


if __name__ == '__main__':
    test = "Denominada en Euskera como Donostia, está "
    test2 = (
        "The 5 French accents;"
        "The cédille (cedilla) Ç ..."
        "The accent aigu (acute accent) é ..."
        "The accent circonflexe (circumflex) â, ê, î, ô, û ..."
        "The accent grave (grave accent) à, è, ù ..."
        "The accent tréma (dieresis/umlaut) ë, ï, ü"
    )
    for t in (test, test2):
        print(filter_accents(t))
