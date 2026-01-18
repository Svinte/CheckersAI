from core.constants import WHITE, BLACK, MAN, KING

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

def evaluate(game_state, perspective):
    score = 0
    for y in range(8):
        for x in range(8):
            p = game_state.board.get(x, y)
            if not p:
                continue

            value = 1 if p.kind == MAN else 3

            # keskusetu
            center_bonus = 0
            if 2 <= x <= 5 and 2 <= y <= 5:
                center_bonus = 0.2

            # korotusetu
            promotion_bonus = 0
            if p.kind == MAN:
                if p.color == WHITE:
                    promotion_bonus = (7 - y) * 0.05
                else:
                    promotion_bonus = y * 0.05

            score += (value + center_bonus + promotion_bonus) * p.color

    return score * perspective

def evaluate_move(before, after, ai_color):
    """
    Pisteytys halutulla säännöllä.
    """
    b1 = count_pieces(before)
    b2 = count_pieces(after)

    score = 0

    # Vastustajan napin syönti
    enemy_eaten = b1[ai_color * -1] - b2[ai_color * -1]
    score += enemy_eaten * 1

    # Oman napin menetys
    own_lost = b1[ai_color] - b2[ai_color]
    score -= own_lost * 1

    # Oman päivitys
    own_kings_before = b1[f"king_{ai_color}"]
    own_kings_after = b2[f"king_{ai_color}"]
    score += (own_kings_after - own_kings_before) * 0.5

    # Vastustajan päivitys
    enemy_kings_before = b1[f"king_{ai_color * -1}"]
    enemy_kings_after = b2[f"king_{ai_color * -1}"]
    score -= (enemy_kings_after - enemy_kings_before) * 0.5

    return score
