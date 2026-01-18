def _minimax_score(self, state, depth):
    if depth == 0:
        return evaluate(state, self.color)
    moves = get_all_moves(state.board, state.turn)
    if not moves:
        return evaluate(state, self.color)

    best = -math.inf
    for m in moves:
        clone = state.clone()
        clone.board.move(m.fx, m.fy, m.tx, m.ty)
        clone.switch_turn()
        best = max(best, self._minimax_score(clone, depth - 1))
    return best
