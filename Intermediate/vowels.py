#! /usr/bin/env python3.13
'''
Finish the get_word_max_vowels function below that takes a text string as its
input argument and returns a tuple of the word that has the most vowels and its
count.

For example running the function on the first paragraph of the Python tutorial:
    Python is an easy to learn, powerful programming language. It has efficient
    high-level data structures and a simple but effective approach to object-
    oriented programming. Python’s elegant syntax and dynamic typing, together
    with its interpreted nature, make it an ideal language for scripting and
    rapid application development in many areas on most platforms.
It returns: ('object-oriented', 6).

In the tests we check 5 paragraphs more of this text. Good luck and have fun!
'''


from collections import defaultdict


VOWELS = list('aeiou')


def get_word_max_vowels(text: str) -> tuple[str, int]:
    """Get the case insensitive word in text that has most vowels.
       Return a tuple of the matching word and the vowel count, e.g.
       ('object-oriented', 6)"""
    tally = defaultdict(int)

    for word in text.strip().split():
        # Skip words already counted:
        if (current := word.lower()) in tally:
            continue
        for letter in (current := word.lower()):
            if letter in VOWELS:
                tally[current] += 1

    return sorted(tally.items(), key=lambda item: item[1], reverse=True)[0]


if __name__ == '__main__':
    test_data = '''
        Python is an easy to learn, powerful programming language. It has efficient
        high-level data structures and a simple but effective approach to object-oriented
        programming. Python's elegant syntax and dynamic typing, together with its
        interpreted nature, make it an ideal language for scripting and rapid application
        development in many areas on most platforms.
    '''
    expected_result = ('object-oriented', 6)
    actual_result = get_word_max_vowels(test_data)

    print(f'Result:\n* {actual_result}')
    assert actual_result == expected_result, 'Uh oh - need more testing...'
