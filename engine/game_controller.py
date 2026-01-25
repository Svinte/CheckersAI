from ai.evaluator import evaluate
from core.game_state import GameState
from ui.classify_move import classify_move
from core.rules import get_all_moves, get_followup_captures


class GameController:
    def __init__(self, white_actor, black_actor):
        self.state = GameState()
        self.last_ai_explanation = []

        self.last_move_feedback = None
        self.last_move_player = None

        self.white_actor = white_actor
        self.black_actor = black_actor
        self.forced_piece = None
        self.last_move = None

    def get_legal_moves(self):
        if self.forced_piece:
            return get_followup_captures(self.state.board, self.forced_piece)
        return get_all_moves(self.state.board, self.state.turn)

    def _compute_move_delta(self, state, move, player_color):
        clone = state.clone()
        clone.board.move(move.fx, move.fy, move.tx, move.ty)

        if abs(move.fx - move.tx) == 2:
            followups = get_followup_captures(clone.board, move)
            if followups:
                return self._compute_best_followup_delta(clone, followups, player_color)

        clone.switch_turn()
        return evaluate(clone, player_color) - evaluate(state, player_color)

    def _compute_best_followup_delta(self, state, followups, player_color):
        best_delta = -float("inf")
        for f in followups:
            clone = state.clone()
            clone.board.move(f.fx, f.fy, f.tx, f.ty)

            further = get_followup_captures(clone.board, f)
            if further:
                delta = self._compute_best_followup_delta(clone, further, player_color)
            else:
                clone.switch_turn()
                delta = evaluate(clone, player_color) - evaluate(state, player_color)

            best_delta = max(best_delta, delta)

        return best_delta

    def _compute_average_delta(self, state, moves, player_color):
        deltas = []
        for m in moves:
            deltas.append(self._compute_move_delta(state, m, player_color))
        return sum(deltas) / len(deltas) if deltas else 0

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

        before = self.state.clone()
        player_color = before.turn

        was_capture = abs(move.fx - move.tx) == 2

        if not is_ai_turn:
            if len(moves) == 1:
                self.last_move_feedback = "Forced"
            else:
                delta = self._compute_move_delta(before, move, player_color)
                avg_delta = self._compute_average_delta(before, moves, player_color)
                self.last_move_feedback = classify_move(delta, avg_delta)

            self.last_move_player = player_color

        self.state.board.move(move.fx, move.fy, move.tx, move.ty)
        self.last_move = move

        if was_capture:
            followups = get_followup_captures(self.state.board, move)
            if followups:
                self.forced_piece = move
                return

        self.forced_piece = None
        self.state.switch_turn()
