#! /usr/bin/env python3.13
'''
An anagram is a word or phrase formed by rearranging the letters of a different
word or phrase, typically using all the original letters exactly once.[1] For
example, the word anagram can be rearranged into "naga ram". Or for example, the
word binary can be rearranged into "brainy". [1]

In this Bite you complete the function below receiving two words and return
True/False if word2 is an anagram of word1. See the tests for some interesting
anagrams. See if you can use a data structure of the standard library.


[1] https://en.wikipedia.org/wiki/Anagram
'''


from collections import Counter
from collections.abc import Callable
from string import punctuation, whitespace


EXTRA = punctuation + whitespace


def is_anagram(word1: str, word2: str) -> bool:
    """Receives two words and returns True/False (boolean) if word2 is
       an anagram of word1, ignore case and spacing.
       About anagrams: https://en.wikipedia.org/wiki/Anagram"""
    prep: Callable[[str], str] = lambda word: word.lower().translate(str.maketrans('', '', EXTRA))

    return Counter(prep(word1)) == Counter(prep(word2))


if __name__ == '__main__':
    examples = [
        ("New York Times", "monkeys write"),
        ("Church of Scientology", "rich-chosen goofy cult"),
        ("McDonald's restaurants", "Uncle Sam's standard rot"),
        ("failure", "completely different"),
        ("coronavirus", "carnivorous"),
        ("She Sells Sanctuary", "Santa; shy, less cruel"),
        ("test", "irrelevant"),
        ("evil", "vile"),
        ("a gentleman", "elegant man"),
        ("silent", "listen"),
    ]
    for word1, word2 in examples:
        print(f'"{word1}" and "{word2}" are anagrams:  {is_anagram(word1, word2)}')
