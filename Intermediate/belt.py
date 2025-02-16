#! /usr/bin/env python3.13
'''
PyBites awards belts based on accrued points from solving Bites ranging from
white (10 points) to red (1,000) points
'''


from bisect import bisect_right


# Globals:
SCORES = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
BELTS = 'white yellow orange green blue brown black paneled red'.split()


def get_belt(user_score: int, scores: list[int]=SCORES, belts: list[str]=BELTS) -> str|None:
    '''
    Receives above arguments and returns a belt

    Alternatively:
    for score, belt in zip(scores[::-1], belts[::-1]):
    if user_score >= score:
        return belt
    '''
    return belts[i - 1] if (i := bisect_right(scores, user_score)) else None

if __name__ == '__main__':
    for user_score in (162, 401, 999):
        print(f'User score:  {user_score},  Belt:  {get_belt(user_score)}')
