#! /usr/bin/env python3.13


class MultiplicationTable:
    def __init__(self, length: int) -> None:
        """Create a 2D self._table of (x, y) coordinates and
           their calculations (form of caching)"""
        self._len = length
        self._table = [[x * y for x in range(1, length + 1)]
                       for y in range(1, length + 1)]

    def __len__(self) -> int:
        """Returns the area of the table (len x * len y)"""
        return self._len * self._len

    def __str__(self) -> str:
        """Returns a string representation of the table"""
        w = len(str(self.__len__()))
        str_table = [[str(col) for col in row]
                     for row in self._table]
        return '\n'.join(' | '.join(row) for row in str_table)

    def __repr__(self) -> str:
        return f'MultiplicationTable({self._len})'

    def calc_cell(self, x, y) -> int:
        """Takes x and y coords and returns the re-calculated result"""
        if 1 > x > self._len or 1 > y > self._len:
            raise IndexError(f'Expected x and y values between 1 - {self._.len}, got {x}, {y}')

        return self._table[y + 1][x + 1]


if __name__ == '__main__':
    multbl = MultiplicationTable(12)
    print(multbl)
