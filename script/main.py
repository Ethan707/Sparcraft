'''
Author: Ethan Chen
Date: 2021-07-15 12:40:17
LastEditTime: 2021-07-21 13:12:45
LastEditors: Ethan Chen
Description: 
FilePath: /Sparcraft/script/main.py
'''
from Game import *
from BUS import *
from evaluation import *
from DSL import *

if __name__ == '__main__':
    # open Sparcraft as subprocess
    game = Game(NOKDPS(), AttackWeakest(), num_exp=1)
    game.run_experiment()
    game.print_result()
    # bound = 10
    # use_triage = False
    # eval_function = PlayWithRandomPlayer(20)
    # algorithm = ButtomUpSearch('', '')
    # algorithm.search(
    #     bound,
    #     [Times, Plus, Minus, Argmax, Argmin, IT, ITE, LT, Equal, Sum, And, Or, Not, Map, Function],
    #     [0, 1, 10],
    #     ['x', 'y', 'z'],
    #     ['num_attacks', 'num_moves', 'num_reload'],
    #     ['moves_distance', 'enemy_distance', 'enemy_hp', 'enemy_range', 'enemy_damage', 'enemy_dpf'],
    #     [],
    #     eval_function,
    #     use_triage
    # )
