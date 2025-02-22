#! /usr/bin/env python3.13
'''
Refactor globals into Enum and:
* Add a __str__ method so each member would print like this: BEGINNER => 👍👍,
  where BEGINNER is the level and the number of thumbs ups the amount of points.
* Write a classmethod called average that returns an average of the scores in
  the Enum.
'''


from enum import Enum

THUMBS_UP = '👍'  # in case you go f-string ...


class Score(Enum):
    BEGINNER = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    CHEATED = 1

    def __str__(self) -> str:
        return f'{self.name} => {THUMBS_UP * self.value}'

    @classmethod
    def average(cls) -> float:
        return sum(i.value for i in cls)/len(cls)


if __name__ == '__main__':
    for i in (Score.CHEATED, Score.BEGINNER, Score.INTERMEDIATE, Score.ADVANCED, 1, 2, 3, 4):
        print(Score(i)) if isinstance(i, int) else print(i)
