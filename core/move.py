class Move:
    def __init__(self, fx, fy, tx, ty):
        self.fx = fx
        self.fy = fy
        self.tx = tx
        self.ty = ty

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (
            self.fx == other.fx and
            self.fy == other.fy and
            self.tx == other.tx and
            self.ty == other.ty
        )

    def __hash__(self):
        return hash((self.fx, self.fy, self.tx, self.ty))
