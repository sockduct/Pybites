#! /usr/bin/env python3.13
'''
In this Bite you complete generate_xmas_tree that takes a rows arg (= height of
the tree). For each row you print row_number*2-1 stars and center them, so for
default height=10 the tree would look like this:

         *
        ***
       *****
      *******
     *********
    ***********
   *************
  ***************
 *****************
*******************

No printing to the console this time, you return this output from the function
(use newlines / \n between the lines). Good luck and keep calm and code in
Python!
'''


from collections.abc import Callable


def generate_xmas_tree(rows: int=10) -> str:
    """Generate a xmas tree of stars (*) for given rows (default 10).
       Each row has row_number*2-1 stars, simple example: for rows=3 the
       output would be like this (ignore docstring's indentation):
         *
        ***
       *****"""
    width: Callable[[int], int] = lambda r: r * 2 - 1
    indent: Callable[[int], int] = lambda r: rows - r
    tree = [f'{" " * indent(row)}{"*" * width(row)}' for row in range(1, rows + 1)]
    return '\n'.join(tree)


if __name__ == '__main__':
    for rows in (3, 10):
        print(generate_xmas_tree(rows))
