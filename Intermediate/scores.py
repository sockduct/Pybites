#! /usr/bin/env python3.13
'''
Complete the two functions below:
*   calculate_score takes a list of dice roll scores and returns the total score
    only taking into account scores of >= MIN_SCORE. If scores contains invalid
    data (!= DICE_VALUES) raise a ValueError.
*   get_winner uses this calculate_score helper to calculate the winning player
    from a list of Player namedtuples. However if the players passed in are not
    having the same number of scores (e.g. all have 4 scores) you should raise a
    ValueError too.

See the docstrings and pytest code for more info. Keep calm and code in Python,
happy Cyber Monday!
'''


from collections import namedtuple


MIN_SCORE = 4
DICE_VALUES = range(1, 7)


Player = namedtuple('Player', 'name scores')


def calculate_score(scores: list[int]) -> int:
    """Based on a list of score ints (dice roll), calculate the
       total score only taking into account >= MIN_SCORE
       (= eyes of the dice roll).

       If one of the scores is not a valid dice roll (1-6)
       raise a ValueError.

       Returns int of the sum of the scores.
    """
    if any((score not in DICE_VALUES) for score in scores):
        raise ValueError(f'Score must in {DICE_VALUES}')

    return sum(score for score in scores if score >= MIN_SCORE)


def get_winner(players: list[Player]) -> Player:
    """Given a list of Player namedtuples return the player
       with the highest score using calculate_score.

       If the length of the scores lists of the players passed in
       don't match up raise a ValueError.

       Returns a Player namedtuple of the winner.
       You can assume there is only one winner.

       For example - input:
         Player(name='player 1', scores=[1, 3, 2, 5])
         Player(name='player 2', scores=[1, 1, 1, 1])
         Player(name='player 3', scores=[4, 5, 1, 2])

       output:
         Player(name='player 3', scores=[4, 5, 1, 2])

    Alternative approach:
    score_lengths = {len(player.scores) for player in players}
    if len(score_lengths) > 1:
        raise ValueError('Players with different amount of score')
    """
    if sum(len(player.scores) for player in players) % len(players) != 0:
        raise ValueError('All players must have the same number of scores')

    return max(players, key=lambda player: calculate_score(player.scores))
