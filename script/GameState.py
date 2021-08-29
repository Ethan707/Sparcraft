'''
Author: Ethan Chen
Date: 2021-07-04 11:22:06
LastEditTime: 2021-08-29 01:08:01
LastEditors: Ethan Chen
Description: Game state class
FilePath: \Sparcraft\script\GameState.py
'''
import numpy as np
from Constant import *


class Unit:
    def __init__(self, position: list, hp: int, range: int, damage: int, dpf: float):
        self.position = position  # [x,y]: the position of the unit
        self.hp = hp              # unit's hp
        self.range = range        # range of unit's weapon
        self.damage = damage      # damage of unit's weapon
        self.dpf = dpf            # unit's dpf

        # format of move: [moveType, moveIndex, position_x, position_y]
        self.moves = []  # avaliable moves for unit

    def setPosition(self, position: list):
        '''function to set unit's position'''
        assert len(position) == 2
        self.position = position

    def setHP(self, hp: int):
        '''function to set unit's hp'''
        self.hp = hp

    def setRange(self, range: int):
        '''function to set the range of unit's weapon'''
        self.range = range

    def setDamage(self, damage: int):
        '''function to set the damage of unit's weapon'''
        self.damage = damage

    def canAttackTarget(self, unit):
        '''function to check wheather the unit could attack the given unit'''
        if self.damage == 0:
            return False
        return (self.range*self.range) >= self.getDistanceToUnit(unit)  # check range

    def getDistanceToPosition(self, position: list):
        '''function to get the distance from unit to given position'''
        return (self.position[0]-position[0])**2+(self.position[1]-position[1])**2

    def getDistanceToUnit(self, unit):
        '''function to get the distance from unit to given unit'''
        return self.getDistanceToPosition(unit.position)

    def getActionsByType(self, type) -> list:
        '''TODO'''
        moves = []
        for move in self.moves:
            if move[0] == type:
                moves.append(move)
        return moves

    def getMoveDistanceList(self) -> list:
        '''TODO'''
        result = []
        moves = self.getActionsByType(MOVE)
        for i in moves:
            result.append(self.getDistanceToPosition([i[-2], i[-1]]))
        return result


class GameState:
    def __init__(self):
        self.time = 0  # game time
        self.player_id = 0  # player id for current round
        self.player_unit = []  # player units for current round
        self.enemy_unit = []  # enemy units for current round

    def getPlayerId(self) -> int:
        '''function to get player id'''
        return self.player_id

    def getEnemy(self, player_id: int) -> int:
        '''function to get enemy units'''
        assert (player_id == 1 or player_id == 0)
        return 1-player_id

    def setTime(self, time):
        '''function to set up game time'''
        self.time = time

    def clear(self):
        '''clear all info for GameState'''
        self.time = 0
        self.player_unit.clear()
        self.enemy_unit.clear()

    def addUnit(self, unit: Unit):
        '''function to add given unit to player units'''
        self.player_unit.append(unit)

    def addEnemy(self, unit: Unit):
        '''function to add given unit to enemy units'''
        self.enemy_unit.append(unit)

    def getUnitByIndex(self, index) -> Unit:
        '''function to get player unit by given index'''
        assert 0 <= index < len(self.player_unit)
        return self.player_unit[index]

    def getEnemyByIndex(self, index) -> Unit:
        '''function to get enemy unit by given index'''
        assert 0 <= index < len(self.enemy_unit)
        return self.enemy_unit[index]

    def getClosestEnemyUnit(self, unit: Unit) -> Unit:
        '''function to get the closest enemy unit by given unit'''
        index = np.argmin([i.getDistanceToUnit(unit) for i in self.enemy_unit])
        return self.getEnemyByIndex(index)

    def getEnemyDistanceFromUnit(self, unit: Unit) -> list:
        '''function to get the distance from given unit to its closest enemy unit'''
        distance = [i.getDistanceToUnit(unit) for i in self.enemy_unit]
        index = [i[1] for i in unit.getActionsByType(ATTACK)]
        return [distance[i] for i in index]

    def getEnemyFromUnit(self, unit: Unit) -> list:
        '''function to get all enemy units by given unit'''
        index = [i[1] for i in unit.getActionsByType(ATTACK)]
        return [self.enemy_unit[i] for i in index]
