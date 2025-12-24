#! /usr/bin/env python3.14


'''
In this Bite you have to complete generate_improved_xmas_tree that takes a rows
arg (= number of rows with leafs). For each row you add a star, leafs and a
trunk and center them nicely. This bite is an extension to Xmas tree generator
with additional elements and some twists.

Elements of the tree:
* STAR: Every tree has exactly one star at the top row.
* LEAF: Every tree has row_number * 2 - 1 leafs per row.
* TRUNK: Every tree has a trunk with a height of 2 and a width which is half of
  the largest leaf row.
    * However, the trunk should always be nicely centered by having the same number
      of empty spaces on both sides of the trunk. Therefore, you have to consider
      the width of the leaf rows and do some conditional rounding :)

The tree with default args should look like this:

         +
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
    |||||||||||
    |||||||||||

Return the finished tree as a multi-line string (use newlines \n between the
lines).

Good luck and keep calm and merry Python Xmas!
'''


STAR = "+"
LEAF = "*"
TRUNK = "|"


from math import ceil


def generate_improved_xmas_tree(rows: int=10) -> str:
    """Generate a xmas tree with a star (+), leafs (*) and a trunk (|)
       for given rows of leafs (default 10).
       For more information see the test and the bite description"""
    if 1 > rows > 99:
        raise ValueError(f'rows must be between 1 - 99, not {rows}')

    width = rows * 2 - 1

    # Alternatively:
    # tree = STAR.center(width) + '\n'
    output = f'{STAR:^{width}}\n'
    for row in range(1, rows + 1):
        count = row * 2 - 1
        output += f'{LEAF * count:^{width}}\n'

    trunk_width = ceil(width/2)
    if trunk_width % 2 == 0 and trunk_width + 1 <= width:
        trunk_width += 1
    output += f'{TRUNK * trunk_width:^{width}}\n'
    output += f'{TRUNK * trunk_width:^{width}}\n'

    return output


if __name__ == '__main__':
    for rows in range(1, 13):
        print(f'Rows = {rows}:')
        print(generate_improved_xmas_tree(rows))
        print()
