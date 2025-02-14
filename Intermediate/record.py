#! /usr/bin/env python3.13
'''
Class to keep track of game score
* Calling class used to pass new score and return max score
Note:  Must also support negative numbers
'''


class RecordScore():
    """Class to track a game's maximum score"""
    def __init__(self) -> None:
        # Alternative:
        # self._score = float('-inf')
        self.score: list[int] = []

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __call__(self, new_score: int) -> int:
        # Alternative:
        # self._score = max(self._score, new_score)
        # return self._score
        self.score.append(new_score)
        return max(self.score)

    def clear(self) -> None:
        self.score = []


if __name__ == '__main__':
    scores = RecordScore()
    print(f'Repr:  {scores!r}')
    for score in (10, 9, 11, None, -5, -10, -2):
        if isinstance(score, int):
            print(f'Record score of {score}:  {scores(score)}')
        else:
            print('Clearing scores...')
            scores.clear()
