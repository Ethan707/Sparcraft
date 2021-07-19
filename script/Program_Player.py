'''
Author: Ethan Chen
Date: 2021-07-19 17:08:29
LastEditTime: 2021-07-19 17:37:44
LastEditors: Ethan Chen
Description: Program player for buttom up search
FilePath: \Sparcraft\script\Program_Player.py
'''


from Constant import *


class ProgramPlayer:
    def __init__(self, program):
        self.program = program
        self.player_id = 0

    def set_player_id(self, player_id):
        self.player_id = player_id

    def init_env(self, unit_state, game_state):
        enemy = game_state.getEnemyFromUnit(unit_state)

        env = {}
        env['game_state'] = game_state
        env['unit_state'] = unit_state
        env['attack_actions'] = unit_state.getActionsByType(ATTACK)
        env['move_actions'] = unit_state.getActionsByType(MOVE)
        env['reload_actions'] = unit_state.getActionsByType(RELOAD)

        env['num_attacks'] = len(env['attack_actions'])
        env['num_moves'] = len(env['move_actions'])
        env['num_reload'] = len(env['reload_actions'])

        # For move
        env['moves_distance'] = unit_state.getMoveDistanceList()
        # destination enemy that could attack

        # For Attack
        env['enemy_distance'] = game_state.getEnemyDistanceFromUnit(unit_state)
        env['enemy_hp'] = [i.hp for i in enemy]
        env['enemy_range'] = [i.range for i in enemy]
        env['enemy_damage'] = [i.damage for i in enemy]
        env['enemy_dpf'] = [i.dpf for i in enemy]

        return env

    def generate(self, state):
        self.state = state
        result = []
        for unit in state.player_unit:
            if len(unit.moves) > 0:
                env = self.init_env(unit, state)
                decision = self.program.interpret(env)
                assert 0 <= decision < len(unit.moves)
                result.append(decision)
        return result
