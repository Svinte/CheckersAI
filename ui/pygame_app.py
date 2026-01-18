import pygame
from core.constants import *
from core.move import Move

CELL = 80
BOARD_SIZE = CELL * 8
SIDE_PANEL = 240
FONT = None

class PygameApp:
    def __init__(self, controller, human_actor=None):
        pygame.init()
        pygame.display.init()
        pygame.font.init()

        global FONT
        FONT = pygame.font.SysFont("Arial", 18)

        self.controller = controller
        self.human = human_actor
        self.selected = None

        self.screen = pygame.display.set_mode((BOARD_SIZE + SIDE_PANEL, BOARD_SIZE))
        pygame.display.set_caption("Checkers AI")
        self.clock = pygame.time.Clock()

    def draw_side_panel(self):
        pygame.draw.rect(
            self.screen,
            (30, 30, 30),
            (BOARD_SIZE, 0, SIDE_PANEL, BOARD_SIZE)
        )

    def draw_ai_info(self):
        explanation = getattr(self.controller, "last_ai_explanation", None)
        if not explanation:
            return

        title = FONT.render("AI moves", True, (255, 255, 255))
        self.screen.blit(title, (BOARD_SIZE + 10, 10))

        y = 40
        for move, score in explanation:
            text = f"{move.fx},{move.fy} -> {move.tx},{move.ty} : {round(score,1)}"
            line = FONT.render(text, True, (200, 200, 200))
            self.screen.blit(line, (BOARD_SIZE + 10, y))
            y += 24

    def draw_last_ai_move(self):
        last = getattr(self.controller, "last_move", None)
        if not last:
            return

        overlay = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))

        self.screen.blit(overlay, (last.fx * CELL, last.fy * CELL))
        self.screen.blit(overlay, (last.tx * CELL, last.ty * CELL))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_side_panel()

        for y in range(8):
            for x in range(8):
                color = (200, 200, 200) if (x + y) % 2 == 0 else (50, 50, 50)
                pygame.draw.rect(self.screen, color, (x * CELL, y * CELL, CELL, CELL))

        self.draw_last_ai_move()

        for y in range(8):
            for x in range(8):
                piece = self.controller.state.board.get(x, y)
                if piece:
                    c = (255, 255, 255) if piece.color == WHITE else (200, 0, 0)
                    pygame.draw.circle(
                        self.screen,
                        c,
                        (x * CELL + CELL // 2, y * CELL + CELL // 2),
                        CELL // 3
                    )

        legal = self.controller.get_legal_moves()
        for m in legal:
            pygame.draw.rect(
                self.screen,
                (0, 0, 255),
                (m.tx * CELL, m.ty * CELL, CELL, CELL),
                2
            )

        if self.selected:
            x, y = self.selected
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (x * CELL, y * CELL, CELL, CELL),
                4
            )

        self.draw_ai_info()

    def handle_click(self, x, y):
        legal = self.controller.get_legal_moves()

        if self.selected is None:
            for m in legal:
                if m.fx == x and m.fy == y:
                    self.selected = (x, y)
                    return
        else:
            move = Move(self.selected[0], self.selected[1], x, y)

            if move in legal:
                self.human.set_move(move)
                self.selected = None
            else:
                self.selected = None

    def run(self):
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = e.pos[0] // CELL, e.pos[1] // CELL
                    self.handle_click(mx, my)

            if not self.controller.state.finished:
                self.controller.step()

            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
