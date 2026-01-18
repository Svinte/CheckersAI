from actors.base_actor import BaseActor

class HumanActor(BaseActor):
    def __init__(self):
        self.pending_move = None

    def set_move(self, move):
        self.pending_move = move

    def choose_move(self, game_state, moves):
        if self.pending_move is None:
            return None
        if self.pending_move in moves:
            move = self.pending_move
            self.pending_move = None
            return move
        return None
