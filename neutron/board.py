from pprint import pprint
from string import ascii_uppercase


class Tile(list):
    def __init__(self, *values):
        super().__init__(list(values) or [])


class Board:
    def __init__(self, x: int, y: int):
        self.board = [{i: {j: Tile() for j in range(y)} for i in ascii_uppercase[:x]}]


    # def __repr__(self):
    #     return '\n'.join([' '.join(map(str, row)) for row in self.board])


b = Board(5, 5)

pprint(b.board)

