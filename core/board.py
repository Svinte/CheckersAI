from core.constants import *
from core.piece import Piece

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self._setup()

    def _setup(self):
        for y in range(3):
            for x in range(BOARD_SIZE):
                if (x + y) % 2 == 1:
                    self.grid[y][x] = Piece(BLACK)

        for y in range(5, 8):
            for x in range(BOARD_SIZE):
                if (x + y) % 2 == 1:
                    self.grid[y][x] = Piece(WHITE)

    def get(self, x, y):
        return self.grid[y][x]

    def move(self, fx, fy, tx, ty):
        piece = self.grid[fy][fx]
        self.grid[fy][fx] = None
        self.grid[ty][tx] = piece

        if abs(fx - tx) == 2:
            mx = (fx + tx) // 2
            my = (fy + ty) // 2
            self.grid[my][mx] = None

        if piece.color == WHITE and ty == 0:
            piece.promote()
        if piece.color == BLACK and ty == BOARD_SIZE - 1:
            piece.promote()
