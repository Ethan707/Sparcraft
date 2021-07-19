from GameState import GameState
import random


class RandomPlayer:
    def __init__(self):
        self.player_id = 0

    def set_player_id(self, player_id):
        self.player_id = player_id

    def generate(self, game: GameState):
        result = []
        for i in range(len(game.player_unit)):
            if len(game.player_unit[i].moves) > 0:
                result.append(random.randint(0, len(game.player_unit[i].moves)-1))
        return result
