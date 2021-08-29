from GameState import GameState
from Constant import *
import random

# The scripted players for Sparcraft
# list:
# 0. Tutorial Player
# 1. Random Player
# 2. Attack Closest
# 3. Attack DPS
# 4. Attack Weakest
# 5. Attack Weakest (No overkill)
# 6. Kiter DPS (No overkill)
# 7. Kiter DPS
# 8. No over kill

# ATTENTION:
# move is different from MOVE !!!
# move: the general description of actions
# MOVE: the "move" action (all the "move" action will be wrote as MOVE)


class Player:
    '''The basic structure for players'''

    def __init__(self):
        self.player_id = 0

    def set_player_id(self, player_id):
        ''' set up the player id for player'''
        self.player_id = player_id

    def generate(self, game: GameState):
        '''generate move decision for the player'''
        raise Exception('Unimplemented method: generate')

# ******************************Tutorials Player Begin******************************


class TutorialsPlayer(Player):
    '''WARNING: DO NOT USE THIS !!!'''

    def generate(self, game: GameState):
        result = []  # contain the index of the moves
        for i in range(len(game.player_unit)):
            if len(game.player_unit[i].moves) > 0:
                # for units with available moves more than 0
                # the legal index that could add to result is from 0 to len(unit.moves)-1
                # each unit could only have one move to executed (ATTACK, MOVE, RELOAD)

                # Do somehing here and add the decision to result
                pass
        return result

# ******************************Tutorials Player End******************************


class RandomPlayer(Player):
    '''
    Chooses a random legal move from each unit
    '''

    def generate(self, game: GameState):
        result = []  # countain the index of the moves
        for i in range(len(game.player_unit)):
            # only the unit with avaliable moves needs to generate move
            # otherwise just ignore it
            if len(game.player_unit[i].moves) > 0:
                result.append(random.randint(0, len(game.player_unit[i].moves)-1))
        return result


class AttackClosest(Player):
    '''
    Chooses an action with following priority:
    1) If it can attack, ATTACK closest enemy unit
    2) If it cannot attack:
        a) If it is in range to attack an enemy, WAIT until can shoot again
        b) If it is not in range of enemy, MOVE towards closest
    '''

    def generate(self, game: GameState):
        result = []
        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)  # get the closest enemy
            foundAction = False
            actionMoveIndex = 0
            closestMoveIndex = 0
            actionDistance = 100000000000
            closestMoveDistance = 100000000000
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]  # get detail of current index of move
                    moveType = move[0]  # MOVE? ATTACK? or RELOAD?
                    # Note:
                    # if the move type is ATTACK, then the moveIndex is the index of target enemy
                    # if the move type is MOVE, then the moveIndex is the index of direction
                    # if the move type is RELOAD, then the moveIndex is 0 (the unit itself)
                    moveIndex = move[1]

                    if moveType == ATTACK:
                        enemy = game.getEnemyByIndex(moveIndex)
                        distance = unit.getDistanceToUnit(enemy)
                        # update the distance and target if we get a smaller one
                        if distance < actionDistance:
                            actionDistance = distance
                            actionMoveIndex = i
                            foundAction = True

                    if moveType == MOVE:
                        # Sparcraft only support 4 default directions
                        # use the index to generate the position
                        position = [unit.position[0]+MOVE_DIR[moveIndex][0],
                                    unit.position[1]+MOVE_DIR[moveIndex][1]]
                        distance = closestEnemy.getDistanceToPosition(position)
                        # MOVE towards closest
                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i
                    # If it is in range to attack an enemy, WAIT until can shoot again
                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break

                result.append(actionMoveIndex if foundAction else closestMoveIndex)  # attack comes first
        return result


class AttackDPS(Player):
    '''
    Chooses an action with following priority:
    1) If it can attack, ATTACK highest DPS/HP enemy unit in range
    2) If it cannot attack:
        a) If it is in range to attack an enemy, WAIT until attack
        b) If it is not in range of enemy, MOVE towards closest
    '''

    def generate(self, game: GameState):
        result = []
        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)  # get the closest enemy
            foundAction = False
            actionMoveIndex = 0
            closestMoveIndex = 0
            actionHighestDPS = 0
            closestMoveDistance = 100000000000
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]  # get detail of current index of move
                    moveType = move[0]  # MOVE? ATTACK? or RELOAD?
                    # Note:
                    # if the move type is ATTACK, then the moveIndex is the index of target enemy
                    # if the move type is MOVE, then the moveIndex is the index of direction
                    # if the move type is RELOAD, then the moveIndex is 0 (the unit itself)
                    moveIndex = move[1]

                    if moveType == ATTACK:
                        enemy = game.getEnemyByIndex(moveIndex)
                        dpsHPValue = enemy.dpf/enemy.hp
                        # update the DPS and target if we get a larger one
                        if dpsHPValue > actionHighestDPS:
                            actionHighestDPS = dpsHPValue
                            actionMoveIndex = i
                            foundAction = True

                    if moveType == MOVE:
                        # Sparcraft only support 4 default directions
                        # use the index to generate the position
                        position = [unit.position[0]+MOVE_DIR[moveIndex][0],
                                    unit.position[1]+MOVE_DIR[moveIndex][1]]
                        distance = closestEnemy.getDistanceToPosition(position)
                        # MOVE towards closest
                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i
                    # If it is in range to attack an enemy, WAIT until can shoot again
                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break

                result.append(actionMoveIndex if foundAction else closestMoveIndex)
        return result


class AttackWeakest(Player):
    '''
    Chooses an action with following priority:
    1) If it can attack, ATTACK least hp enemy unit
    2) If it cannot attack:
        a) If it is in range to attack an enemy, WAIT
        b) If it is not in range of enemy, MOVE towards closest
    '''

    def generate(self, game: GameState):
        result = []
        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)  # get the closest enemy
            foundAction = False
            actionMoveIndex = 0
            closestMoveIndex = 0
            actionLowestHP = 100000000000
            closestMoveDistance = 100000000000
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]  # get detail of current index of move
                    moveType = move[0]  # MOVE? ATTACK? or RELOAD?
                    # Note:
                    # if the move type is ATTACK, then the moveIndex is the index of target enemy
                    # if the move type is MOVE, then the moveIndex is the index of direction
                    # if the move type is RELOAD, then the moveIndex is 0 (the unit itself)
                    moveIndex = move[1]

                    if moveType == ATTACK:
                        enemy = game.getEnemyByIndex(moveIndex)
                        # update the HP and target if we get a smaller one
                        if enemy.hp < actionLowestHP:
                            actionLowestHP = enemy.hp
                            actionMoveIndex = i
                            foundAction = True

                    if moveType == MOVE:
                        # Sparcraft only support 4 default directions
                        # use the index to generate the position
                        position = [unit.position[0]+MOVE_DIR[moveIndex][0],
                                    unit.position[1]+MOVE_DIR[moveIndex][1]]
                        distance = closestEnemy.getDistanceToPosition(position)
                        # MOVE towards closest
                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i
                    # If it is in range to attack an enemy, WAIT until can shoot again
                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break

                result.append(actionMoveIndex if foundAction else closestMoveIndex)
        return result


class AttackWeakestNOK(Player):
    '''
    Chooses an action with following priority:
    1) If it can attack, ATTACK least hp enemy unit to overkill
    2) If it cannot attack:
        a) If it is in range to attack an enemy, WAIT
        b) If it is not in range of enemy, MOVE towards closest
    '''

    def generate(self, game: GameState):
        result = []
        remainingHP = [enemy.hp for enemy in game.enemy_unit]  # the list to record the remaining hp of enemies

        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)
            foundAction = False
            actionMoveIndex = 0
            closestMoveIndex = 0
            actionLowestHP = 100000000000
            closestMoveDistance = 100000000000
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]  # get detail of current index of move
                    moveType = move[0]  # MOVE? ATTACK? or RELOAD?
                    # Note:
                    # if the move type is ATTACK, then the moveIndex is the index of target enemy
                    # if the move type is MOVE, then the moveIndex is the index of direction
                    # if the move type is RELOAD, then the moveIndex is 0 (the unit itself)
                    moveIndex = move[1]

                    # only attack the enemy with remaining hp more than 0
                    if moveType == ATTACK and remainingHP[moveIndex] > 0:
                        # update the HP and target if we get a smaller one
                        if remainingHP[moveIndex] < actionLowestHP:
                            actionLowestHP = remainingHP[moveIndex]
                            actionMoveIndex = i
                            foundAction = True

                    if moveType == MOVE:
                        # Sparcraft only support 4 default directions
                        # use the index to generate the position
                        position = [unit.position[0]+MOVE_DIR[moveIndex][0],
                                    unit.position[1]+MOVE_DIR[moveIndex][1]]
                        distance = closestEnemy.getDistanceToPosition(position)
                        # MOVE towards closest
                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i
                    # If it is in range to attack an enemy, WAIT until can shoot again
                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break
                bestMoveIndex = actionMoveIndex if foundAction else closestMoveIndex
                # if the unit chooses to ATTACK at last, update the enemies' remaning hp
                bestMove = unit.moves[bestMoveIndex]
                if bestMove[0] == ATTACK:
                    remainingHP[bestMove[1]] -= unit.damage
                result.append(bestMoveIndex)
        return result


class Kiter_NOKDPS(Player):
    '''
    Chooses an action with following priority:
    1) If it can attack, ATTACK highest DPS/HP enemy unit to overkill
    2) If it cannot attack:
        a) If it is in range to attack an enemy, WAIT until attack
        b) If it is not in range of enemy, MOVE towards closest
    '''

    def generate(self, game: GameState):
        result = []
        remainingHP = [enemy.hp for enemy in game.enemy_unit]  # the list to record the remaining hp of enemies

        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)
            foundAction = False
            actionMoveIndex = 0
            furthestMoveIndex = 0
            furthestMoveDistance = 0
            actionHighestDPS = 0
            closestMoveIndex = 0
            closestMoveDistance = 100000000000
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]  # get detail of current index of move
                    moveType = move[0]  # MOVE? ATTACK? or RELOAD?
                    # Note:
                    # if the move type is ATTACK, then the moveIndex is the index of target enemy
                    # if the move type is MOVE, then the moveIndex is the index of direction
                    # if the move type is RELOAD, then the moveIndex is 0 (the unit itself)
                    moveIndex = move[1]

                    # only attack the enemy with remaining hp more than 0
                    if moveType == ATTACK and remainingHP[moveIndex] > 0:
                        enemy = game.getEnemyByIndex(moveIndex)
                        dpsHPValue = enemy.dpf/enemy.hp
                        # update the DPS and target if we get a larger one
                        if dpsHPValue > actionHighestDPS:
                            actionHighestDPS = dpsHPValue
                            actionMoveIndex = i
                            foundAction = True

                    if moveType == MOVE:
                        # Sparcraft only support 4 default directions
                        # use the index to generate the position
                        position = [unit.position[0]+MOVE_DIR[moveIndex][0],
                                    unit.position[1]+MOVE_DIR[moveIndex][1]]
                        distance = closestEnemy.getDistanceToPosition(position)

                        # Record the furthest one
                        if distance > furthestMoveDistance:
                            furthestMoveDistance = distance
                            furthestMoveIndex = i
                        # Record the closest one
                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i

                    # If it is in range to attack an enemy, WAIT until attack
                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break

                # Attack comes first
                if foundAction:
                    bestMoveIndex = actionMoveIndex
                else:
                    # if it can attack the closest enemy, move away from it
                    # if it can not attack the closest enemy, move toward to it
                    bestMoveIndex = furthestMoveIndex if unit.canAttackTarget(closestEnemy) else closestMoveIndex

                # if the unit chooses to ATTACK at last, update the enemies' remaning hp
                bestMove = unit.moves[bestMoveIndex]
                if bestMove[0] == ATTACK:
                    remainingHP[bestMove[1]] -= unit.damage
                result.append(bestMoveIndex)
        return result


class Kiter_DPS(Player):
    '''
    Chooses an action with following priority:
    1) If it can attack, ATTACK highest DPS/HP enemy unit in range
    2) If it cannot attack:
        a) If it is in range to attack an enemy, move away from closest one
        b) If it is not in range of enemy, MOVE towards closest one
    '''

    def generate(self, game: GameState):
        result = []

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
                    move = unit.moves[i]  # get detail of current index of move
                    moveType = move[0]  # MOVE? ATTACK? or RELOAD?
                    # Note:
                    # if the move type is ATTACK, then the moveIndex is the index of target enemy
                    # if the move type is MOVE, then the moveIndex is the index of direction
                    # if the move type is RELOAD, then the moveIndex is 0 (the unit itself)
                    moveIndex = move[1]

                    if moveType == ATTACK:
                        enemy = game.getEnemyByIndex(moveIndex)
                        dpsHPValue = enemy.dpf/enemy.hp
                        # update the DPS and target if we get a larger one
                        if dpsHPValue > actionHighestDPS:
                            actionHighestDPS = dpsHPValue
                            actionMoveIndex = i
                            foundAction = True

                    if moveType == MOVE:
                        # Sparcraft only support 4 default directions
                        # use the index to generate the position
                        position = [unit.position[0]+MOVE_DIR[moveIndex][0],
                                    unit.position[1]+MOVE_DIR[moveIndex][1]]
                        distance = closestEnemy.getDistanceToPosition(position)

                        # Record the furthest one
                        if distance > furthestMoveDistance:
                            furthestMoveDistance = distance
                            furthestMoveIndex = i

                        # Record the closest one
                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i

                    # If it is in range to attack an enemy, WAIT until attack
                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break

                # Attack comes first
                if foundAction:
                    bestMoveIndex = actionMoveIndex
                else:
                    # if it can attack the closest enemy, move away from it
                    # if it can not attack the closest enemy, move toward to it
                    bestMoveIndex = furthestMoveIndex if unit.canAttackTarget(closestEnemy) else closestMoveIndex

                result.append(bestMoveIndex)
        return result


class NOKDPS(Player):
    '''
    Chooses an action with following priority:
    1) If it can attack, ATTACK highest DPS/HP enemy unit to overkill
    2) If it cannot attack:
        a) If it is in range to attack an enemy, WAIT until attack
        b) If it is not in range of enemy, MOVE towards closest
    '''

    def generate(self, game: GameState):
        result = []
        remainingHP = [enemy.hp for enemy in game.enemy_unit]  # the list to record the remaining hp of enemies

        for unit in game.player_unit:
            closestEnemy = game.getClosestEnemyUnit(unit)
            foundAction = False
            actionMoveIndex = 0
            closestMoveIndex = 0
            actionHighestDPS = 0
            closestMoveDistance = 100000000000
            if len(unit.moves) > 0:
                for i in range(len(unit.moves)):
                    move = unit.moves[i]  # get detail of current index of move
                    moveType = move[0]  # MOVE? ATTACK? or RELOAD?
                    # Note:
                    # if the move type is ATTACK, then the moveIndex is the index of target enemy
                    # if the move type is MOVE, then the moveIndex is the index of direction
                    # if the move type is RELOAD, then the moveIndex is 0 (the unit itself)
                    moveIndex = move[1]

                    # only attack the enemy with remaining hp more than 0
                    if moveType == ATTACK and remainingHP[moveIndex] > 0:
                        enemy = game.enemy_unit[moveIndex]
                        dpsHPValue = enemy.dpf/enemy.hp
                        # update the DPS and target if we get a larger one
                        if dpsHPValue > actionHighestDPS:
                            actionHighestDPS = dpsHPValue
                            actionMoveIndex = i
                            foundAction = True

                    if moveType == MOVE:
                        # Sparcraft only support 4 default directions
                        # use the index to generate the position
                        position = [unit.position[0]+MOVE_DIR[moveIndex][0],
                                    unit.position[1]+MOVE_DIR[moveIndex][1]]
                        distance = closestEnemy.getDistanceToPosition(position)
                        # MOVE towards closest
                        if distance < closestMoveDistance:
                            closestMoveDistance = distance
                            closestMoveIndex = i

                    # If it is in range to attack an enemy, WAIT until attack
                    if moveType == RELOAD:
                        if unit.canAttackTarget(closestEnemy):
                            closestMoveIndex = i
                            break

                bestMoveIndex = actionMoveIndex if foundAction else closestMoveIndex
                # if the unit chooses to ATTACK at last, update the enemies' remaning hp
                bestMove = unit.moves[bestMoveIndex]
                if bestMove[0] == ATTACK:
                    remainingHP[bestMove[1]] -= unit.damage
                result.append(bestMoveIndex)
        return result
