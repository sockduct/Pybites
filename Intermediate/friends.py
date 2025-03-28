#! /usr/bin/env python3.13
'''
In this Bite you are presented with a users dict of keys=id's and
values=usernames and a friendships list of user ID tuples expressing a
friendship between two users.

Loop through friendships and find out which user has the most friends. Return a
tuple of friend name and his or her friends. Have fun!
'''


from collections import defaultdict


names = 'bob julian tim martin rod sara joyce nick beverly kevin'.split()
ids = range(len(names))
users = dict(zip(ids, names))  # 0: bob, 1: julian, etc

friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3),
               (3, 4), (4, 5), (5, 6), (5, 7), (5, 9),
               (6, 8), (7, 8), (8, 9)]


def get_friend_with_most_friends(friendships: list[tuple[int, int]],
                                 users: dict[int, str]=users) -> tuple[str, list[str]]:
    """Receives the friendships list of user ID pairs,
       parse it to see who has most friends, return a tuple
       of (name_friend_with_most_friends, his_or_her_friends)"""
    frset = defaultdict(set)
    for friendship in friendships:
        frset[friendship[0]].add(friendship[1])
        frset[friendship[1]].add(friendship[0])

    person, friends = sorted(frset.items(), key=lambda item: len(item[1]), reverse=True)[0]

    return users[person], [users[friend] for friend in friends]


if __name__ == '__main__':
    print('The friend with the most friends is:\n'
          f'{get_friend_with_most_friends(friendships, users)}')
