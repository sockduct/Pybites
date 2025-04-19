#! /usr/bin/env python3.13
'''
In this Bite you are presented with a list of car (manufacturer, model) tuples.
Group the data by manufacturer printing the following table output of
MANUFACTURER + bullet list of car models.

This is the truncated output you are expected to deliver (see the tests for the
full output):

CHEVROLET
- Cavalier
- Corvette
- Impala

...

MERCEDES-BENZ
- 300D
- 600SEL
- E-Class

...

VOLKSWAGEN
- GTI
- Passat
- Routan

As you see both manufacturers and models are alphabetically ordered.

You might want to check out itertools.groupby for this one, but there are
probably more ways to do it. Have fun and keep calm and code in Python!
'''


from collections.abc import Iterator
from itertools import groupby
from operator import itemgetter


cars = [
    # need mock data? -> https://www.mockaroo.com == awesome
    ('Mercedes-Benz', '300D'), ('Mercedes-Benz', '600SEL'),
    ('Toyota', 'Avalon'), ('Ford', 'Bronco'),
    ('Chevrolet', 'Cavalier'), ('Chevrolet', 'Corvette'),
    ('Mercedes-Benz', 'E-Class'), ('Hyundai', 'Elantra'),
    ('Volkswagen', 'GTI'), ('Toyota', 'Highlander'),
    ('Chevrolet', 'Impala'), ('Nissan', 'Maxima'),
    ('Ford', 'Mustang'), ('Kia', 'Optima'),
    ('Volkswagen', 'Passat'), ('Nissan', 'Pathfinder'),
    ('Volkswagen', 'Routan'), ('Hyundai', 'Sonata'),
    ('Kia', 'Sorento'), ('Kia', 'Sportage'),
    ('Ford', 'Taurus'), ('Nissan', 'Titan'),
    ('Toyota', 'Tundra'), ('Hyundai', 'Veracruz'),
]


def group_cars_by_manufacturer(
        cars: list[tuple[str, str]], *, display: bool=True
    ) -> Iterator[tuple[str, Iterator[tuple[str, str]]]]|None:
    """Iterate though the list of (manufacturer, model) tuples
       of the cars list defined above and generate the output as described
       in the Bite description (see the tests for the full output).

       No return here, just print to the console. We use pytest > capfd to
       validate your output :)
    """
    # sorted_cars = sorted(cars, key=lambda car: (car[0], car[1]))
    # Instead use - can't use inline though because sort is in-place with no return:
    cars.sort()
    # result = groupby(cars, key=lambda car: car[0])
    # Instead use:
    result = groupby(cars, key=itemgetter(0))

    if not display:
        return result

    for mfg, grouping in result:
        print(f'{mfg.upper()}')
        for mfg, model in grouping:
            print(f'- {model}')
        print()

    # To make mypy happy:
    return None


if __name__ == '__main__':
    group_cars_by_manufacturer(cars)
