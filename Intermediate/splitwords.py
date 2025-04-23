#! /usr/bin/env python3.13
'''
Another text manipulation Bite. Code split_words_and_quoted_text that takes a
text string and splits it by space, except words that are wrapped between double
quotes ("), these spaces needs to be preserved.

So passing it:  Should give "3 words only", it would return a list of 3 (not 5)
elements: ['Should', 'give', '3 words only'] (note that the double quotes are
stripped off as well).

Check out the standard library, there might be a tool for the job ;) - good luck
and keep calm and code in Python!
'''


from shlex import split


def split_words_and_quoted_text(text: str) -> list[str]:
    """Split string text by space unless it is
       wrapped inside double quotes, returning a list
       of the elements.

       For example
       if text =
       'Should give "3 elements only"'

       the resulting list would be:
       ['Should', 'give', '3 elements only']
    """
    return split(text)


if __name__ == '__main__':
    print(split_words_and_quoted_text('Should give "3 elements only"'))
