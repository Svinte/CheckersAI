from core.constants import MAN, KING

class Piece:
    def __init__(self, color, kind=MAN):
        self.color = color
        self.kind = kind

    def promote(self):
        self.kind = KING
