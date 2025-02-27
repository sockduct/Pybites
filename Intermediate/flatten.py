#! /usr/bin/env python3.13
'''
Flatten any nested sequence container - list/tuple/deque with nested list(s)/
tuple(s)/deque(s) into a single sequence container

Can return a list or a generator
'''


from collections import deque
from collections.abc import Iterator
from typing import Any, TypeVar


# Define all sequence type containers
# array.array can't be nested and other sequences are not containers
SEQ = (list, tuple, deque)
type SEQ_T = list[Any] | tuple[Any, ...] | deque[Any]
SEQ_TVar = TypeVar('SEQ_TVar', list[Any], tuple[Any, ...], deque[Any])


# def flatten(list_of_lists: SEQ, *, generator: bool=False) -> SEQ|Iterator[Any]:
def flatten(list_of_lists: SEQ_T) -> Iterator[Any]:
    for element in list_of_lists:
        if isinstance(element, (SEQ)):
            yield from flatten(element)
        else:
            yield element


def flatten_type(seqcontainer: SEQ_TVar) -> SEQ_TVar:
    if not isinstance(seqcontainer, SEQ):
        raise TypeError(f'Expected ", ".join(SEQ) got: "{type(seqcontainer).__name__}"')

    res = flatten(seqcontainer)
    return (
        list(res) if isinstance(seqcontainer, list) else
        tuple(res) if isinstance(seqcontainer, tuple) else
        deque(res)
    )


if __name__ == '__main__':
    test_list = [1, [2, 3], [4, 5, [6, 7, [8, 9, 10]]]]
    output1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert flatten_type(test_list) == output1, 'Error:  Incorrect response from flatten.'

    test_tuple = (1, (2, 3), (4, 5, (6, 7, (8, 9, 10))))
    output2 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    assert flatten_type(test_tuple) == output2, 'Error:  Incorrect response from flatten.'

    test_deque = deque([1, deque([2, 3]), deque([4, 5, deque([6, 7, deque([8, 9, 10])])])])
    output3 = deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert flatten_type(test_deque) == output3, 'Error:  Incorrect response from flatten.'
