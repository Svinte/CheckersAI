from core.game_state import GameState
from core.rules import get_all_moves, get_followup_captures

class GameController:
    def __init__(self, white_actor, black_actor):
        self.state = GameState()
        self.last_ai_explanation = []
        self.white_actor = white_actor
        self.black_actor = black_actor
        self.forced_piece = None
        self.last_move = None

    def get_legal_moves(self):
        if self.forced_piece:
            return get_followup_captures(self.state.board, self.forced_piece)
        return get_all_moves(self.state.board, self.state.turn)

    def step(self):
        if self.state.finished:
            return

        actor = self.white_actor if self.state.turn == 1 else self.black_actor
        moves = self.get_legal_moves()

        if not moves:
            self.state.finished = True
            return

        is_ai_turn = hasattr(actor, "ai") and actor.ai is not None

        if is_ai_turn and hasattr(actor.ai, "explain"):
            self.last_ai_explanation = actor.ai.explain(self.state, moves)

        move = actor.choose_move(self.state, moves)
        if move is None or move not in moves:
            return

        was_capture = abs(move.fx - move.tx) == 2

        self.state.board.move(move.fx, move.fy, move.tx, move.ty)

        self.last_move = move

        if was_capture:
            followups = get_followup_captures(self.state.board, move)
            if followups:
                self.forced_piece = move
                return

        self.forced_piece = None
        self.state.switch_turn()
