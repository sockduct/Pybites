#! /usr/bin/env python3.13


import random


names = ['Julian', 'Bob', 'PyBites', 'Dante', 'Martin', 'Rodolfo']
aliases = ['Pythonista', 'Nerd', 'Coder'] * 2
points = random.sample(range(81, 101), 6)
awake = [True, False] * 3
SEPARATOR = ' | '


def generate_table(*args):
    return [SEPARATOR.join(str(seqelem) for seqelem in zipseq) for zipseq in zip(*args)]


if __name__ == '__main__':
    print(generate_table(names))
    print(generate_table(names, aliases))
    print(generate_table(names, aliases, points))
    print(generate_table(names, aliases, points, awake))
