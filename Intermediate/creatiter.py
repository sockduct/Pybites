#! /usr/bin/env python3.13
'''
Create an iterator
* iterable - "streaming" capable object like sequences with __iter__ or
  __getitem__ methods; iterable objects passed to iter() built-in return a
  single-pass iterator for the object
* iterator - object representing datastream; calls to iterator's __next__ or
  next() built-in return next item in stream; when stream exhausted,
  StopIteration is raised; iterators must have __iter__ method which returns
  object itself (so every iterator is iterable); Note:  Some iterables like
  lists produce new iterator each time passed to iter()

Note:  Don't make an object (class) an iterator for itself (implement __next__).
       Doing so prevents multiple traversals of object.  Instead, the class
       should return a separate iterator.  One way to do this is by using a
       generator function/expression.  Can also create iterator class which
       implements __iter__ and __next__ if for some reason don't want to use
       generators.
'''


from collections.abc import Iterator
from random import choice
from typing import Self


COLORS = 'red blue green yellow brown purple'.split()


class EggCreator:
    '''
    * Parameters:
      * limit: int => max number of eggs to create
    * Return:
      * Eggs of randomly chosen colors (from COLOR) => str: <color> egg
    '''
    def __init__(self, limit: int) -> None:
        self.__current = 0
        self.limit = limit

    def __iter__(self) -> Iterator[str]:
        # return EggCreatorIterator(self.limit)
        # This is potentially an antipattern but doing so as tests require:
        return self

    def __next__(self) -> str:
        # This is potentially an antipattern but doing so as tests require:
        self.__current += 1
        if self.__current <= self.limit:
            return self.__str__()
        else:
            raise StopIteration()

    def __repr__(self) -> str:
        return f'EggCreator({self.limit})'

    def __str__(self) -> str:
        return f'{choice(COLORS)} egg'


class EggCreatorIterator:
    def __init__(self, limit: int, start: int=0) -> None:
        self.__current = start
        self.limit = limit

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> str:
        self.__current += 1
        if self.__current <= self.limit:
            return f'{choice(COLORS)} egg'
        else:
            raise StopIteration()

    def __repr__(self) -> str:
        return f'EggCreatorIterator({self.limit}, {self.__current})'


if __name__ == '__main__':
    egg = EggCreator(4)
    print(f'egg repr:  {egg!r}')
    print(f'egg str:  {egg}')
    print(f'egg iteration:  {", ".join(egg)}', end='')
