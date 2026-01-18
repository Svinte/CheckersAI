from actors.base_actor import BaseActor

class AIActor(BaseActor):
    def __init__(self, ai):
        self.ai = ai

    def choose_move(self, game_state, moves):
        return self.ai.choose_move(game_state, moves)
