#! /usr/bin/env python3.13


from abc import ABC, abstractmethod


class Challenge(ABC):
    def __init__(self, number, title):
        self.number = number
        self.title = title

    @property
    @abstractmethod
    def verify(self):
        pass


class BlogChallenge(Challenge):
    pass


class BiteChallenge(Challenge):
    pass
