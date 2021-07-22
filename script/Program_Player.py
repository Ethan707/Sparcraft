'''
Author: Ethan Chen
Date: 2021-07-19 17:08:29
LastEditTime: 2021-07-22 20:20:23
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

    def init_env(self, game):
        env = {}
        env['state'] = game
        return env

    def generate(self, state):
        env = self.init_env(state)
        return self.program.interpret(env)
