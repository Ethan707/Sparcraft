from GameState import GameState, ATTACK, MOVE, RELOAD, MOVE_DIR


class AttackClosest:
    def __init__(self, palyer_id):
        self.palyer_id = palyer_id

    def generate(self, game: GameState):
        result = []
        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)
            foundAction = False
            actionMoveIndex = 0
            closestMoveIndex = 0
            actionDistance = 100000000000
            closestMoveDistance = 100000000000
            # format of move: [moveType, moveIndex, position_x, position_y]
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]
                    moveType = move[0]
                    moveIndex = move[1]

                    if moveType == ATTACK:
                        enemy = game.enemy_unit[moveIndex]
                        distance = unit.getDistanceToUnit(enemy)
                        if distance < actionDistance:
                            actionDistance = distance
                            actionMoveIndex = i
                            foundAction = True

                    if moveType == MOVE:
                        position = [unit.position[0]+MOVE_DIR[moveIndex][0],
                                    unit.position[1]+MOVE_DIR[moveIndex][1]]
                        assert len(position) == 2
                        distance = closestEnemy.getDistanceToPosition(position)
                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i

                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break

                result.append(actionMoveIndex if foundAction else closestMoveIndex)
        return result
