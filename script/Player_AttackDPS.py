'''
Author: Ethan Chen
Date: 2021-07-05 07:10:58
LastEditTime: 2021-07-05 09:55:39
LastEditors: Ethan Chen
Description: Attack enemy based on DPS
FilePath: \Sparcraft\script\Player_AttackDPS.py
'''
from GameState import GameState
from Constant import *


class AttackDPS:
    def __init__(self, player_id):
        self.player_id = player_id

    def generate(self, game: GameState):
        result = []
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

                    if moveType == ATTACK:
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
                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i

                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break

                result.append(actionMoveIndex if foundAction else closestMoveIndex)
        return result
