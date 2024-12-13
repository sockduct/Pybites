#! /usr/bin/env python3.13


from itertools import combinations, permutations
from typing import Iterator, Sequence


def friends_teams(friends: Sequence[str], team_size: int=2,
                  order_does_matter: bool=False) -> Iterator[tuple[str, ...]]:
    '''
    * Alternatively - more DRY:
    if order_does_matter:
        func = itertools.permutations
    else:
        func = itertools.combinations
    return func(friends, team_size)
    '''
    if order_does_matter:
        return permutations(friends, team_size)
    else:
        return combinations(friends, team_size)
