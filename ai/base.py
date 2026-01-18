class BaseAI:
    def choose_move(self, game_state, moves):
        raise NotImplementedError

    def explain(self, game_state, moves):
        raise NotImplementedError
