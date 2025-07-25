#! /usr/bin/env python3.13
'''
In this Bite you will complete the group function that receives an iterable and
splits it up in n groups. Say we have a list of 10 ints and n=3, passing this
into the function you'd get the following return:
>>> iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> n = 3
>>> from grouping import group
>>> group(iterable, n)
[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

It should also work passing in a generator:
>>> iterable = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
>>> group(iterable, n)
[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

And of course for different values for iterable and n (see also the tests):
>>> iterable = [1, 2, 3, 4] * 3
>>> iterable
[1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
>>> group(iterable, 2)
[[1, 2], [3, 4], [1, 2], [3, 4], [1, 2], [3, 4]]

Thanks to Andrew (CodeItch) for letting us know about this code/idea derived
from one of Sumo Logic's repos.
'''


from collections.abc import Iterable
from itertools import islice
from typing import Any


def group(iterable: Iterable[Any], n: int) -> list[list[Any]]:
    """Splits an iterable set into groups of size n and a group
       of the remaining elements if needed.

       Args:
         iterable (list): The list whose elements are to be split into
                          groups of size n.
         n (int): The number of elements per group.

       Returns:
         list: The list of groups of size n,
               where each group is a list of n elements.
    """
    # Consider type checking iterable and cast to generator if necessary:
    # if not isinstance(iterable, types.GeneratorType):
    #     iterable = (i for i in iterable)
    # But not sure if that's needed with iter builtin...

    # Nope - test is for list of lists:
    # return list(batched(iterable, n))
    res = []
    iterator = iter(iterable)
    while group := list(islice(iterator, n)):
        res.append(group)

    return res


if __name__ == '__main__':
    iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    n = 3
    ret = group(iterable, n)
    print(ret)
