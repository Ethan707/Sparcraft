'''
Author: Ethan Chen
Date: 2021-07-04 11:22:06
LastEditTime: 2021-07-05 16:30:17
LastEditors: Ethan Chen
Description: Game state class
FilePath: \Sparcraft\script\GameState.py
'''
import numpy as np
from Constant import *
# const int SparCraft::Constants::Move_Dir[4][2] = {{-1, 0}, {1, 0}, {0, 1}, {0, -1}}


class Unit:
    def __init__(self, position: list, hp: int, range: int, damage: int, dpf: float):
        self.position = position
        self.hp = hp
        self.range = range
        self.damage = damage
        self.dpf = dpf
        # format of move: [moveType, moveIndex, position_x, position_y]
        self.moves = []

    def setPosition(self, position: list):
        assert len(position) == 2
        self.position = position

    def setHP(self, hp: int):
        self.hp = hp

    def setRange(self, range: int):
        self.range = range

    def setDamage(self, damage: int):
        self.damage = damage

    def canAttackTarget(self, unit):
        if self.damage == 0:
            return False
        return (self.range*self.range) >= self.getDistanceToUnit(unit)

    def getDistanceToPosition(self, position: list):
        return (self.position[0]-position[0])**2+(self.position[1]-position[1])**2

    def getDistanceToUnit(self, unit):
        return self.getDistanceToPosition(unit.position)


class GameState:
    def __init__(self):
        self.time = 0
        self.player_unit = []
        self.enemy_unit = []

    def getEnemy(self, player_id: int) -> int:
        assert (player_id == 1 or player_id == 0)
        return 1-player_id

    def setTime(self, time):
        self.time = time

    def clear(self):
        self.time = 0
        self.player_unit.clear()
        self.enemy_unit.clear()

    def addUnit(self, unit: Unit):
        self.player_unit.append(unit)

    def addEnemy(self, unit: Unit):
        self.enemy_unit.append(unit)

    def getUnitByIndex(self, index) -> Unit:
        assert 0 <= index < len(self.player_unit)
        return self.player_unit[index]

    def getEnemyByIndex(self, index) -> Unit:
        assert 0 <= index < len(self.enemy_unit)
        return self.enemy_unit[index]

    def getClosestEnemyUnit(self, unit: Unit) -> Unit:
        index = np.argmin([i.getDistanceToUnit(unit) for i in self.enemy_unit])
        return self.getEnemyByIndex(index)
