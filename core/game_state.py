from core.board import Board
from core.constants import WHITE
import copy

class GameState:
    def __init__(self):
        self.board = Board()
        self.turn = WHITE
        self.finished = False

    def switch_turn(self):
        self.turn *= -1

    def clone(self):
        return copy.deepcopy(self)
