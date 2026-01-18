from core.constants import *
from core.move import Move

MAN_DIRS = {
    WHITE: [(-1, -1), (1, -1)],
    BLACK: [(-1, 1), (1, 1)]
}

KING_DIRS = [(-1, -1), (1, -1), (-1, 1), (1, 1)]


def get_all_moves(board, color):
    captures = []
    moves = []

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            piece = board.get(x, y)
            if not piece or piece.color != color:
                continue

            caps = get_captures(board, x, y)
            if caps:
                captures.extend(caps)
            elif not captures:
                moves.extend(get_simple_moves(board, x, y))

    return captures if captures else moves


def get_simple_moves(board, x, y):
    piece = board.get(x, y)
    result = []
    dirs = KING_DIRS if piece.kind == KING else MAN_DIRS[piece.color]

    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if board.get(nx, ny) is None:
                result.append(Move(x, y, nx, ny))

    return result


def get_captures(board, x, y):
    piece = board.get(x, y)
    result = []
    dirs = KING_DIRS if piece.kind == KING else MAN_DIRS[piece.color]

    for dx, dy in dirs:
        mx, my = x + dx, y + dy
        tx, ty = x + 2*dx, y + 2*dy

        if not (0 <= tx < BOARD_SIZE and 0 <= ty < BOARD_SIZE):
            continue

        middle = board.get(mx, my)
        if middle and middle.color != piece.color and board.get(tx, ty) is None:
            result.append(Move(x, y, tx, ty))

    return result


def get_followup_captures(board, move):
    return get_captures(board, move.tx, move.ty)
