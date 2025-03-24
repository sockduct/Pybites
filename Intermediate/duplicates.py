#! /usr/bin/env python3.13
'''
In this Bite you are presented with a list of words. Loop through them and find
all the words that are duplicated. Of those return the (0-based) indices of the
first occurrence.

Example 1: In the following list 'is' and 'it' occur more than once, and they
are at indices 0 and 1 so you would return [0, 1]:
    * ['is', 'it', 'true', 'or', 'is', 'it', 'not?'] => [0, 1]

Example 2: Because this, new, and bite are duplicated and are at index 0, 3 and
4 respectively:
    * ['this', 'is', 'a', 'new', 'bite', 'I', 'hope', 'this', 'bite', 'will',
       'teach', 'you', 'something', 'new'] => [0, 3, 4]
'''


from collections import Counter


def get_duplicate_indices(words: list[str]) -> list[int]:
    """
    Given a list of words, loop through the words and check for each word if it
    occurs more than once. If so return the index of its first occurrence.

    Make sure the returning list is unique and sorted in ascending order.
    """
    count = Counter(words)
    duplicates = {key: value for key, value in count.items() if value > 1}
    indices = [words.index(key) for key in duplicates]

    return sorted(indices)


if __name__ == '__main__':
    for example in (
        ['is', 'it', 'true', 'or', 'is', 'it', 'not?'],
        [
            'this', 'is', 'a', 'new', 'bite', 'I', 'hope', 'this', 'bite', 'will',
            'teach', 'you', 'something', 'new'
        ]
    ):
        print(f'{example} => {get_duplicate_indices(example)}')
