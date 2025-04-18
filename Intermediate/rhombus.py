#! /usr/bin/env python3.13
'''
In this Bite you make a generator of rhombus shapes. You will complete
gen_rhombus that when called like this:

    gen = gen_rhombus(5)  # gen_rhombus is a generator
    for row in gen:
        print(row)

... will generate the following output:

  *
 ***
*****
 ***
  *

When called with a greater width (you only have to worry about uneven widths for
this exercise):

    gen = gen_rhombus(11)
    for row in gen:
        print(row)

... the output would be:

     *
    ***
   *****
  *******
 *********
***********
 *********
  *******
   *****
    ***
     *
So the middle row is always equal to the width passed in. Checkout how format or
f-strings can help you here, as well as the range builtin. Have fun!
'''


from collections.abc import Iterator


STAR = '*'


def gen_rhombus(width: int) -> Iterator[str]:
    """Create a generator that yields the rows of a rhombus row
       by row. So if width = 5 it should generate the following
       rows one by one:

       gen = gen_rhombus(5)
       for row in gen:
           print(row)

        output:
          *
         ***
        *****
         ***
          *
    """
    if width % 2 == 0:
        raise ValueError(f'width must be an odd number, not {width}')

    for line in range(1, width + 1, 2):
        yield f'{STAR * line:^{width}}'
    for line in range(width - 2, 0, -2):
        yield f'{STAR * line:^{width}}'


if __name__ == '__main__':
    for size in range(1, 12, 2):
        print(f'Size of {size}:\n{"\n".join(gen_rhombus(size))}')
    # Raises exception:
    next(gen_rhombus(2))
