import random
from ai.base import BaseAI

class RandomAI(BaseAI):
    def choose_move(self, game_state, moves):
        return random.choice(moves)
