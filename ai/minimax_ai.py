from ai.base import BaseAI
from core.rules import get_all_moves, get_followup_captures
from ai.evaluator import evaluate, evaluate_move
import math


class MinimaxAI(BaseAI):
    def __init__(self, depth=3):
        self.depth = depth
        self.color = None

    def explain(self, game_state, moves):
        self.color = game_state.turn

        explanation = []
        for move in moves:
            clone = game_state.clone()
            clone.board.move(move.fx, move.fy, move.tx, move.ty)

            if abs(move.fx - move.tx) == 2:
                followups = get_followup_captures(clone.board, move)
                if followups:
                    score = self._minimax(clone, followups, self.depth, False)
                else:
                    clone.switch_turn()
                    score = self._minimax(clone, None, self.depth - 1, False)
            else:
                clone.switch_turn()
                score = self._minimax(clone, None, self.depth - 1, False)

            explanation.append((move, score))

        return explanation

    def choose_move(self, game_state, moves):
        # Asetetaan AI väri
        self.color = game_state.turn

        best_score = -math.inf
        best_move = None

        for move in moves:
            clone = game_state.clone()
            clone.board.move(move.fx, move.fy, move.tx, move.ty)

            # delta
            delta = evaluate_move(game_state, clone, self.color)

            if abs(move.fx - move.tx) == 2:
                followups = get_followup_captures(clone.board, move)
                if followups:
                    score = delta + self._minimax(clone, followups, self.depth, False)
                else:
                    clone.switch_turn()
                    score = delta + self._minimax(clone, None, self.depth - 1, False)
            else:
                clone.switch_turn()
                score = delta + self._minimax(clone, None, self.depth - 1, False)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, state, forced_moves, depth, maximizing):
        if depth == 0 or state.finished:
            return evaluate(state, self.color)

        if forced_moves is None:
            moves = get_all_moves(state.board, state.turn)
        else:
            moves = forced_moves

        if not moves:
            state.finished = True
            return evaluate(state, self.color)

        if maximizing:
            best = -math.inf
            for m in moves:
                clone = state.clone()
                clone.board.move(m.fx, m.fy, m.tx, m.ty)

                delta = evaluate_move(state, clone, self.color)

                if abs(m.fx - m.tx) == 2:
                    followups = get_followup_captures(clone.board, m)
                    if followups:
                        val = delta + self._minimax(clone, followups, depth, True)
                    else:
                        clone.switch_turn()
                        val = delta + self._minimax(clone, None, depth - 1, False)
                else:
                    clone.switch_turn()
                    val = delta + self._minimax(clone, None, depth - 1, False)

                best = max(best, val)

            return best

        else:
            best = math.inf
            for m in moves:
                clone = state.clone()
                clone.board.move(m.fx, m.fy, m.tx, m.ty)

                delta = evaluate_move(state, clone, self.color)

                if abs(m.fx - m.tx) == 2:
                    followups = get_followup_captures(clone.board, m)
                    if followups:
                        val = delta + self._minimax(clone, followups, depth, False)
                    else:
                        clone.switch_turn()
                        val = delta + self._minimax(clone, None, depth - 1, True)
                else:
                    clone.switch_turn()
                    val = delta + self._minimax(clone, None, depth - 1, True)

                best = min(best, val)

            return best
