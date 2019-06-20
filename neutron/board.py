import math
from pprint import pprint
from string import ascii_uppercase

from numpy import median


class Board:
    def __init__(self, x: int, y: int):
        if x % 2 == 0 or y % 2 == 0:
            raise ValueError('x and y must be uneven')
        elif x < 3 or y < 3 or x > 26 or y > 26:
            raise ValueError('x and y must be 3 >= x|y =< 26')

        self._x = x
        self._y = y

        for i in ascii_uppercase[:y]:
            if i == ascii_uppercase[0]:
                setattr(self, i, {j: Token(self, 'O') for j in range(x)})
            elif i == ascii_uppercase[x - 1]:
                setattr(self, i, {j: Token(self, 'X') for j in range(x)})
            elif i == ascii_uppercase[int(median(range(y)))]:
                setattr(self, i,
                        {j: Token(self, None) if j != median(range(x)) else Token(self, 'N') for j in range(x)})
            else:
                setattr(self, i, {j: Token(self, None) for j in range(y)})


    @property
    def y(self):
        return tuple(i for i in vars(self) if not i.startswith('_'))


    def x(self, y):
        return getattr(self, str(y))


    def free(self, y, x) -> bool:
        return not self.x(y).get(x)


    def __repr__(self):
        head = "\t".join(self.y)
        index = tuple(range(self._x))
        board = list([i] + [k for k in self.x(ascii_uppercase[i]).values()] for i in index)
        return '\t{head}\n{rows}'.format(head=head, rows='\n'.join(['\t'.join(map(str, n)) for n in board]))


class Token:
    def __init__(self, board: Board, symbol: str = None):
        self.board = board
        self.symbol = symbol


    def __repr__(self):
        return f'[{self.symbol}]' if self.symbol is not None else '[ ]'

    # def move_up(self):
    #     for i in range(self.y, board.y)


for i in range(3, 26, 2):
    print(Board(i, i))
    print()
