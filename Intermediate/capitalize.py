#! /usr/bin/env python3.13
'''
In this Bite you are going to capitalize sentences in a block of lowercased
text.

Correct grammar dictates that each sentence should start with a capital letter,
so complete capitalize_sentences to do just that.

To make this a bit harder we have sentences ending with dot (.), question mark
(?) and exclamation mark (!)
'''


import re


def capitalize_sentences(text: str) -> str:
    """Return text capitalizing the sentences. Note that sentences can end
       in dot (.), question mark (?) and exclamation mark (!)"""
    return re.sub(r'([a-z]).*?[.?!](?:\s+|$)', lambda m: m.group(0).capitalize(), text)


if __name__ == '__main__':
    for test in (
        'this is a test. let\'s see how this does. will it work?  i hope so!',
        'one sentence. another sentence! a third sentence too?'
    ):
        res = capitalize_sentences(test)
        print(f'Before:  {test}\n After:  {res}\n')
