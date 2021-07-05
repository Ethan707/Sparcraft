'''
Author: Ethan Chen
Date: 2021-07-05 07:42:29
LastEditTime: 2021-07-05 09:45:56
LastEditors: Ethan Chen
Description: None
FilePath: \Sparcraft\script\Player_NOKDPS.py
'''
from GameState import GameState
from Constant import *


class NOKDPS:
    def __init__(self, player_id):
        self.player_id = player_id

    def generate(self, game: GameState):
        result = []
        remainingHP = [enemy.hp for enemy in game.enemy_unit]

        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)
            foundAction = False
            actionMoveIndex = 0
            closestMoveIndex = 0
            actionHighestDPS = 0
            closestMoveDistance = 100000000000
            # format of move: [moveType, moveIndex, position_x, position_y]
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]
                    moveType = move[0]
                    moveIndex = move[1]

                    if moveType == ATTACK and remainingHP[moveIndex] > 0:
                        enemy = game.enemy_unit[moveIndex]
                        dpsHPValue = enemy.dpf/enemy.hp
                        if dpsHPValue > actionHighestDPS:
                            actionHighestDPS = dpsHPValue
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

                bestMoveIndex = actionMoveIndex if foundAction else closestMoveIndex
                bestMove = unit.moves[bestMoveIndex]
                if bestMove[0] == ATTACK:
                    remainingHP[bestMove[1]] -= unit.damage
                result.append(bestMoveIndex)
        return result
