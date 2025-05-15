#! /usr/bin/env python3.13
'''
In this Bite you will parse a multiline string of SWAPI Starwars characters.

Calculate the BMI of each character returning a (person, BMI) tuple of the
character that has the highest BMI.

The BMI calculation is the same as Add a command line interface to our BMI
calculator: float(mass) / ((int(height) / 100) ** 2).

The provided data contains 3 columns separated by comma: person, height, and
mass.

Have fun and keep calm and code in Python!
'''


from collections.abc import Callable
from operator import itemgetter


data = """Luke Skywalker,172,77
          C-3PO,167,75
          R2-D2,96,32
          Darth Vader,202,136
          Leia Organa,150,49
          Owen Lars,178,120
          Beru Whitesun lars,165,75
          R5-D4,97,32
          Biggs Darklighter,183,84
          Obi-Wan Kenobi,182,77
          Anakin Skywalker,188,84
          Chewbacca,228,112
          Han Solo,180,80
          Greedo,173,74
          Jek Tono Porkins,180,110
          Yoda,66,17
          Palpatine,170,75
          Boba Fett,183,78.2
          IG-88,200,140
          Bossk,190,113
"""


def person_max_bmi(data: str=data) -> tuple[str, float]:
    """Return (name, BMI float) of the character in data that
       has the highest BMI (rounded on 2 decimals)"""
    bmi: Callable[[str, str], float] = (
        lambda height, mass: round(float(mass) / ((int(height) / 100) ** 2), 2)
    )
    entries = {}
    for line in data.splitlines():
        name, height, mass = line.strip().split(',')
        entries[name] = bmi(height, mass)

    return max(entries.items(), key=itemgetter(1))


if __name__ == '__main__':
    print(person_max_bmi())
