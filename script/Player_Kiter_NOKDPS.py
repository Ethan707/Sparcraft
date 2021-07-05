'''
Author: Ethan Chen
Date: 2021-07-05 07:40:47
LastEditTime: 2021-07-05 09:54:55
LastEditors: Ethan Chen
Description: None
FilePath: \Sparcraft\script\Player_Kiter_NOKDPS.py
'''
from GameState import GameState
from Constant import *


class Kiter_NOKDPS:
    def __init__(self, player_id):
        self.player_id = player_id

    def generate(self, game: GameState):
        result = []
        remainingHP = [enemy.hp for enemy in game.enemy_unit]

        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)
            foundAction = False
            actionMoveIndex = 0
            furthestMoveIndex = 0
            furthestMoveDistance = 0
            actionHighestDPS = 0
            closestMoveIndex = 0
            closestMoveDistance = 100000000000
            # format of move: [moveType, moveIndex, position_x, position_y]
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]
                    moveType = move[0]
                    moveIndex = move[1]

                    if moveType == ATTACK and remainingHP[moveIndex] > 0:
                        enemy = game.getEnemyByIndex(moveIndex)
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

                        if distance > furthestMoveDistance:
                            furthestMoveDistance = distance
                            furthestMoveIndex = i

                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i

                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break

                if foundAction:
                    bestMoveIndex = actionMoveIndex
                else:
                    bestMoveIndex = furthestMoveIndex if unit.canAttackTarget(closestEnemy) else closestMoveIndex

                bestMove = unit.moves[bestMoveIndex]
                if bestMove[0] == ATTACK:
                    remainingHP[bestMove[1]] -= unit.damage
                result.append(bestMoveIndex)
        return result
