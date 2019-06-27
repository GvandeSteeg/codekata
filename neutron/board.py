import math
from pprint import pprint
from string import ascii_uppercase

from numpy import median


class Board:
    def __init__(self, row: int, column: int):
        if row % 2 == 0 or column % 2 == 0:
            raise ValueError('row and column must be uneven')
        elif row < 3 or column < 3 or row > 26 or column > 26:
            raise ValueError('row and column must be 3 >= row|column =< 26')

        self._row = row
        self._column = column

        for i in ascii_uppercase[:column]:
            if i == ascii_uppercase[0]:
                setattr(self, i, {j: Token(self, j, i, 'O') for j in range(row)})
            elif i == ascii_uppercase[row - 1]:
                setattr(self, i, {j: Token(self, j, i, 'X') for j in range(row)})
            elif i == ascii_uppercase[int(median(range(column)))]:
                setattr(self, i,
                        {j: Token(self, j, i, None) if j != median(range(row)) else Token(self, j, i, 'N') for j in
                         range(row)})
            else:
                setattr(self, i, {j: Token(self, j, i, None) for j in range(column)})


    @property
    def column(self):
        return tuple(i for i in vars(self) if not i.startswith('_'))


    def row(self, column):
        return getattr(self, str(column))


    def free(self, column, row) -> bool:
        return not self.row(column).get(row)


    def __repr__(self):
        head = "\t".join(self.column)
        index = tuple(range(self._row))
        board = list([i] + [k for k in self.row(ascii_uppercase[i]).values()] for i in index)
        return '\t{head}\n{rows}'.format(head=head, rows='\n'.join(['\t'.join(map(str, n)) for n in board]))


class Token:
    def __init__(self, board: Board, row: int, column: int, scolumnmbol: str = None):
        self.board = board
        self.row = row
        self.column = column
        self.scolumnmbol = scolumnmbol


    def __repr__(self):
        return f'[{self.scolumnmbol}]' if self.scolumnmbol is not None else '[ ]'


    @property
    def location(self):
        return self.column, self.row


    def move_up(self):
        for i in range(self.row, self.board._row, -1):
            print(i)


b = Board(5, 5)
print(b)
print(b.row('A')[4].move_up())
