'''
Author: Ethan Chen
Date: 2021-07-26 01:20:30
LastEditTime: 2021-07-26 01:27:28
LastEditors: Ethan Chen
Description: 
FilePath: /Sparcraft/script/Player_AttackWeakestNOK.py
'''

from GameState import GameState
from Constant import *


class AttackWeakestNOK:
    def __init__(self):
        self.player_id = 0

    def set_player_id(self, player_id):
        self.player_id = player_id

    def generate(self, game: GameState):
        result = []
        remainingHP = [enemy.hp for enemy in game.enemy_unit]

        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)
            foundAction = False
            actionMoveIndex = 0
            closestMoveIndex = 0
            actionLowestHP = 100000000000
            closestMoveDistance = 100000000000
            # format of move: [moveType, moveIndex, position_x, position_y]
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]
                    moveType = move[0]
                    moveIndex = move[1]

                    if moveType == ATTACK and remainingHP[moveIndex] > 0:
                        enemy = game.getEnemyByIndex(moveIndex)
                        # distance = unit.getDistanceToUnit(enemy)
                        if remainingHP[moveIndex] < actionLowestHP:
                            actionLowestHP = remainingHP[moveIndex]
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
