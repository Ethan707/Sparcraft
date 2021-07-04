from GameState import GameState


class AttackClosest:
    def __init__(self, palyer_id):
        self.palyer_id = palyer_id

    def generate(self, game: GameState):
        result = []
        for unit in game.player_unit:
            if len(unit.moves) > 0:
                for move in unit.moves:
                    pass

        return result
