from ai.base import BaseAI
from core.rules import get_all_moves, get_followup_captures
from ai.evaluator import evaluate
import math
import os
import json
from concurrent.futures import ProcessPoolExecutor, as_completed


def _board_key(board):
    s = []
    for y in range(8):
        for x in range(8):
            p = board.get(x, y)
            if not p:
                s.append("0")
            else:
                s.append(f"{p.color}{p.kind}")
    return "".join(s)


def _evaluate_root_move(args):
    ai, game_state, move = args

    clone = game_state.clone()
    clone.board.move(move.fx, move.fy, move.tx, move.ty)

    clone.switch_turn()
    score = ai._minimax(clone, ai.depth - 1, -math.inf, math.inf)

    return move, score


class MinimaxAI(BaseAI):
    def __init__(self, depth=3, parallel=False, max_workers=None, cache_file="cache.json"):
        self.depth = depth
        self.parallel = parallel
        self.max_workers = max_workers or os.cpu_count()
        self.color = None

        self.cache_file = cache_file
        self.cache = {}
        self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                self.cache = json.load(f)

    def save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f)

    def explain(self, game_state, moves):
        self.color = game_state.turn

        if not self.parallel or len(moves) < 2:
            return self._explain_serial(game_state, moves)

        explanation = []

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(_evaluate_root_move, (self, game_state, move))
                for move in moves
            ]

            for f in as_completed(futures):
                explanation.append(f.result())

        return explanation

    def _explain_serial(self, game_state, moves):
        explanation = []

        for move in moves:
            clone = game_state.clone()
            clone.board.move(move.fx, move.fy, move.tx, move.ty)
            clone.switch_turn()

            score = self._minimax(clone, self.depth - 1, -math.inf, math.inf)
            explanation.append((move, score))

        return explanation

    def choose_move(self, game_state, moves):
        self.color = game_state.turn

        if not self.parallel or len(moves) < 2:
            return self._choose_move_serial(game_state, moves)

        best_score = -math.inf
        best_move = None

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(_evaluate_root_move, (self, game_state, move))
                for move in moves
            ]

            for f in as_completed(futures):
                move, score = f.result()
                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move

    def _choose_move_serial(self, game_state, moves):
        best_score = -math.inf
        best_move = None

        for move in moves:
            clone = game_state.clone()
            clone.board.move(move.fx, move.fy, move.tx, move.ty)
            clone.switch_turn()

            score = self._minimax(clone, self.depth - 1, -math.inf, math.inf)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, state, depth, alpha, beta):
        assert depth >= 0

        moves = get_all_moves(state.board, state.turn)

        key = (
            _board_key(state.board),
            state.turn,
            depth
        )
        if key in self.cache:
            return self.cache[key]

        if depth == 0 or not moves:
            val = evaluate(state, self.color)
            self.cache[key] = val
            return val

        maximizing = (state.turn == self.color)

        # kevyt move ordering: syönnit ensin, ei ilmaisia
        moves.sort(key=lambda m: abs(m.fx - m.tx) == 2, reverse=True)

        if maximizing:
            value = -math.inf
            for m in moves:
                clone = state.clone()
                clone.board.move(m.fx, m.fy, m.tx, m.ty)

                followups = (
                    get_followup_captures(clone.board, m)
                    if abs(m.fx - m.tx) == 2
                    else None
                )

                if followups:
                    val = self._minimax(clone, depth - 1, alpha, beta)
                else:
                    clone.switch_turn()
                    val = self._minimax(clone, depth - 1, alpha, beta)

                value = max(value, val)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

        else:
            value = math.inf
            for m in moves:
                clone = state.clone()
                clone.board.move(m.fx, m.fy, m.tx, m.ty)

                followups = (
                    get_followup_captures(clone.board, m)
                    if abs(m.fx - m.tx) == 2
                    else None
                )

                if followups:
                    val = self._minimax(clone, depth - 1, alpha, beta)
                else:
                    clone.switch_turn()
                    val = self._minimax(clone, depth - 1, alpha, beta)

                value = min(value, val)
                beta = min(beta, value)
                if beta <= alpha:
                    break

        self.cache[key] = value
        return value
