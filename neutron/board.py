import math
from pprint import pprint
from string import ascii_uppercase

from numpy import median


class Board:
    def __init__(self, row: int, column: int):
        if row % 2 == 0 or column % 2 == 0:
            raise ValueError('row and column must be uneven')
        elif row < 3 or column < 3 or row > 26 or column > 26:
            raise ValueError('row and column must be 3 >= row/column <= 26')

        self._row = row
        self._column = column

        for i in ascii_uppercase[:row]:
            if i == ascii_uppercase[0]:
                setattr(self, i, {j: Token(self, i, j, 'O') for j in range(1, column + 1)})
            elif i == ascii_uppercase[row - 1]:
                setattr(self, i, {j: Token(self, i, j, 'X') for j in range(1, column + 1)})
            elif i == ascii_uppercase[int(median(range(row)))]:
                setattr(self, i,
                        {j: Token(self, i, j, None) if j != median(range(1, column + 1)) else Token(self, i, j, 'N') for
                         j in range(1, column + 1)})
            else:
                setattr(self, i, {j: Token(self, i, j, None) for j in range(1, column + 1)})


    @property
    def rows(self):
        return tuple(ascii_uppercase[:self._row])


    @property
    def columns(self):
        return tuple(i + 1 for i in range(self._column))


    def column(self, column: int):
        """

        :param column: visual index, not list index, so 1+
        """
        return tuple(self.row(i)[column - 1] for i in self.rows)


    def row(self, row: str):
        return getattr(self, row)


    def free(self, row, column) -> bool:
        return not self.find(row, column).symbol


    def find(self, row, column):
        return self.row(row).get(column)


    def __repr__(self):
        columns = "\t".join(map(str, self.columns))
        board = [[i] + list(self.row(i).values()) for i in self.rows]
        return '\t{columns}\n{rows}'.format(columns=columns, rows='\n'.join(['\t'.join(map(str, n)) for n in board]))


class Token:
    def __init__(self, board: Board, row: int, column: int, symbol: str = None):
        self.board = board
        self.row = row
        self.column = column
        self.symbol = symbol


    def __repr__(self):
        return f'[{self.symbol}]' if self.symbol is not None else '[ ]'


    @property
    def location(self):
        return self.row, self.column

    # TODO board needs to not have states, states should be token specific!
    def swap(self, target):
        tmp_row = target.row
        tmp_col = target.column
        target.row = self.row
        target.column = self.column
        self.row = tmp_row
        self.column = tmp_col


    def move_up(self):
        for i in ascii_uppercase[ascii_uppercase.index(self.row) - 1::-1]:
            if self.board.free(i, self.column):
                self.swap(self.board.find(i, self.column))
            else:
                break


b = Board(5, 5)
print(b)
print(b.find('E', 1).move_up())
print(b)
