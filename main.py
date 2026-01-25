import multiprocessing
from engine.game_controller import GameController
from actors.ai_actor import AIActor
from actors.human_actor import HumanActor
from ui.pygame_app import PygameApp
from ai.minimax_ai import MinimaxAI


def main():
    human = HumanActor()
    ai = AIActor(MinimaxAI(depth=7, parallel=True, max_workers=10))

    game = GameController(
        white_actor=human,
        black_actor=ai
    )

    app = PygameApp(game, human)
    app.run()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
