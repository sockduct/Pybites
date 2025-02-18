#! /usr/bin/env python3.13


from functools import reduce


def common_languages(programmers: dict[str, list[str]]) -> set[str]:
    """
    Receive a dict of keys -> names and values -> a sequence of
    of programming languages, return the common languages

    Alternative solution:
    return set.intersection(*[set(vals) for vals in programmers.values()])
    """
    return reduce(set.intersection, map(set, programmers.values()))
