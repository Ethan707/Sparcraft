class Unit:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.hp = 0
        self.firstTimeFree = 0
        self.moves = []

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setFirstTimeFree(self, time):
        self.firstTimeFree = time

    def setHP(self, hp):
        self.hp = hp


class GameState:
    def __init__(self):
        self.time = 0
        self.player_unit = []
        self.enemy_unit = []

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

    def getUnitByIndex(self, index):
        assert 0 <= index < len(self.player_unit)
        return self.player_unit[index]
