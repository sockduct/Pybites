#! /usr/bin/env python3.13


class MultiplicationTable:
    def __init__(self, length: int) -> None:
        """Create a 2D self._table of (x, y) coordinates and
           their calculations (form of caching)"""
        self._len = length
        axis = range(1, length + 1)
        self._table = [[x * y for x in axis] for y in axis]

    def __len__(self) -> int:
        """Returns the area of the table (len x * len y)"""
        return self._len * self._len

    def __str__(self) -> str:
        """Returns a basic string representation of the table"""
        str_table = [[str(col) for col in row]
                     for row in self._table]
        return '\n'.join(' | '.join(row) for row in str_table)

    def __repr__(self) -> str:
        return f'MultiplicationTable({self._len})'

    def calc_cell(self, x: int, y: int) -> int:
        """Takes x and y coords and returns the re-calculated result"""
        if not(1 <= x <= self._len and 1 <= y <= self._len):
            raise IndexError(f'Expected x and y values between 1 - {self._len}, got {x}, {y}')

        return self._table[y - 1][x - 1]

    def pprint(self) -> str:
        """Returns prettier string representation of the table"""
        w = len(str(self.__len__()))
        output = ''
        for row in self._table:
            for pos, col in enumerate(row, 1):
                output += f'{col:3}'
                output += ' | ' if pos % self._len != 0 else '\n'
        return output


if __name__ == '__main__':
    print(f'Basic formatting:\n{MultiplicationTable(4)}')
    multbl = MultiplicationTable(16)
    print(f'\nPrettier formatting:\n{multbl.pprint()}')
    print(multbl.calc_cell(16, 16))
    try:
        print(multbl.calc_cell(17, 16))
    except IndexError as err:
        print(err)
    try:
        print(multbl.calc_cell(0, 5))
    except IndexError as err:
        print(err)
    try:
        print(multbl.calc_cell(3, -5))
    except IndexError as err:
        print(err)
    print(multbl.calc_cell(11, 8))
