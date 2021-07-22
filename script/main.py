'''
Author: Ethan Chen
Date: 2021-07-15 12:40:17
LastEditTime: 2021-07-22 21:17:45
LastEditors: Ethan Chen
Description: 
FilePath: \Sparcraft\script\main.py
'''
from Game import *
from BUS import *
from evaluation import *
from dsl_bus import *
from simulated_annealing import *

if __name__ == '__main__':
    # open Sparcraft as subprocess
    # game = Game(NOKDPS(0), AttackWeakest(1))
    # game.print_result()
    bound = 100
    use_triage = True
    eval_function = PlayWithRandomPlayer(10)
    # algorithm = ButtomUpSearch('', '')
    # algorithm.search(
    #     bound,
    #     [Times, Plus, Minus, Argmax, Argmin, IT, ITE, LT, Sum,  Map, Function],
    #     [-1, 0, 1, 2, 10],
    #     ['x'],
    #     ['num_attacks', 'num_moves', 'num_reload'],
    #     ['moves_distance', 'enemy_distance', 'enemy_hp', 'enemy_range', 'enemy_damage', 'enemy_dpf'],
    #     [LTD_Score,
    #      LTD2_Score,
    #      LTD2_PlayerOverOpponent,
    #      LTD2_PlayerOverOpponent,
    #      HasAttackActions,
    #      HasMoveActions,
    #      HasReloadActions],
    #     eval_function,
    #     use_triage
    # )
    algorithm = SimulatedAnnealing('', '')

    terminals = [LTD_Score,
                 LTD_Score,
                 LTD2_Score,
                 LTD2_PlayerOverOpponent,
                 LTD2_PlayerOverOpponent,
                 HasAttackActions,
                 HasMoveActions,
                 HasReloadActions]
    algorithm.search([Times, Plus, Minus, Argmax, Argmin, IT, ITE, LT, Sum,  Map, Function],
                     [],
                     [],
                     [],
                     ['num_attacks', 'num_moves', 'num_reload'],
                     ['moves_distance', 'enemy_distance', 'enemy_hp', 'enemy_range', 'enemy_damage', 'enemy_dpf'],
                     terminals,
                     eval_function,
                     use_triage,

                     float(100),
                     float(0.6),
                     float(100),
                     120)
