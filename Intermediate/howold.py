#! /usr/bin/env python3.13
'''
Ever wondered how old an actor/actress was in a particular movie? In this Bite
you will write some code to find the answer.

Here is how it should work (the Actor and Movie dataclasses are provided):
  (Pdb) actor
  Actor(name='Wesley Snipes', born='July 31, 1962')
  (Pdb) movie
  Movie(title='New Jack City', release_date='January 17, 1991')
  (Pdb) get_age(actor, movie)
  'Wesley Snipes was 28 years old when New Jack City came out.'
  ...
  (Pdb) actor
  Actor(name='Jennifer Aniston', born='February 11, 1969')
  (Pdb) movie
  Movie(title='Horrible Bosses', release_date='September 16, 2011')
  (Pdb) get_age(actor, movie)
  'Jennifer Aniston was 42 years old when Horrible Bosses came out.'

You might want to look into using dateutil to make this a lot easier :)

Keep calm and code in Python!
'''


from dataclasses import dataclass

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


@dataclass
class Actor:
    name: str
    born: str


@dataclass
class Movie:
    title: str
    release_date: str


def get_age(actor: Actor, movie: Movie) -> str:
    """Calculates age of actor / actress when movie was released,
       return a string like this:

       {name} was {age} years old when {movie} came out.
       e.g.
       Wesley Snipes was 28 years old when New Jack City came out.
    """
    age = relativedelta(parse(movie.release_date), parse(actor.born)).years
    return f'{actor.name} was {age} years old when {movie.title} came out.'


if __name__ == '__main__':
    for actor, movie, expected in (
        (Actor(name='Wesley Snipes', born='July 31, 1962'),
         Movie(title='New Jack City', release_date='January 17, 1991'),
         28),
        (Actor(name='Jennifer Aniston', born='February 11, 1969'),
         Movie(title='Horrible Bosses', release_date='September 16, 2011'),
         42)
    ):
        print(f'{actor=}\n{movie=}\nActor age at release:  {get_age(actor, movie)},'
              f'  Expected:  {expected}')
