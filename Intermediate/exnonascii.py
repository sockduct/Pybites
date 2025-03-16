#! /usr/bin/env python3.13
'''
In this Bite you extract words from a text that contain non-ascii characters.
Examples:
* 'Fichier non trouvé' => ['trouvé']

* extract_non_ascii_words('He wonede at Ernleȝe at æðelen are chirechen it') =>
  ['Ernleȝe', 'æðelen']


To do:
* Strip out punctuation
'''

from string import ascii_letters, digits, punctuation


def extract_non_ascii_words(text: str) -> list[str]:
    """Filter a text returning a list of non-ascii words"""
    ascii_set = set(ascii_letters)
    extra = punctuation + digits
    # Easier alternative:  return [word for word in text.split() if not word.isascii()]
    return [word for word in text.split()
            if any(char for char in word.strip(extra) if char not in ascii_set)]


if __name__ == '__main__':
    for test_data in ('Fichier non trouvé', 'He wonede at Ernleȝe at æðelen are chirechen it'):
        print(extract_non_ascii_words(test_data))
