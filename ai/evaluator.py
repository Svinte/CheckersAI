from core.constants import WHITE, BLACK, MAN, KING
from core.rules import get_all_moves, get_followup_captures


def count_pieces(state):
    counts = {
        1: 0,
        -1: 0,
        "king_1": 0,
        "king_-1": 0
    }

    for y in range(8):
        for x in range(8):
            p = state.board.get(x, y)
            if not p:
                continue

            counts[p.color] += 1
            if p.kind == KING:
                counts[f"king_{p.color}"] += 1

    return counts


def is_safe_square(x, y):
    return x == 0 or x == 7 or y == 0 or y == 7


def is_back_row(y, color):
    return (color == WHITE and y == 7) or (color == BLACK and y == 0)


def build_attack_map(board, opponent):
    """
    Palauttaa setin (x,y) ruuduista, jotka vastustaja voi syödä seuraavaksi.
    """
    attack = set()
    moves = get_all_moves(board, opponent)

    for m in moves:
        if abs(m.fx - m.tx) == 2:
            attack.add((m.tx, m.ty))

    return attack


def evaluate(game_state, perspective):
    score = 0

    pieces = count_pieces(game_state)
    if pieces[perspective] == 0:
        return -100
    if pieces[-perspective] == 0:
        return 100

    my_moves = len(get_all_moves(game_state.board, perspective))
    enemy_moves = len(get_all_moves(game_state.board, -perspective))
    score += (my_moves - enemy_moves) * 0.15

    enemy_attack = build_attack_map(game_state.board, -perspective)

    for y in range(8):
        for x in range(8):
            p = game_state.board.get(x, y)
            if not p:
                continue

            value = 1 if p.kind == MAN else 3

            promotion_bonus = 0
            if p.kind == MAN:
                if p.color == WHITE:
                    promotion_bonus = (7 - y) * 0.05
                else:
                    promotion_bonus = y * 0.05

            safe_bonus = 0.05 if is_safe_square(x, y) else 0

            back_row_bonus = 0
            if p.kind == MAN and is_back_row(y, p.color):
                back_row_bonus = 0.2

            exposed_penalty = 0
            if (x, y) in enemy_attack:
                exposed_penalty = 1.1

            score += (
                value
                + promotion_bonus
                + safe_bonus
                + back_row_bonus
                - exposed_penalty
            ) * p.color

    return score * perspective
