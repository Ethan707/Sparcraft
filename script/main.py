'''
Author: Ethan Chen
Date: 2021-07-15 12:40:17
LastEditTime: 2021-07-19 16:26:50
LastEditors: Ethan Chen
Description: 
FilePath: \Sparcraft\script\main.py
'''
from Game import *
from BUS import *
from evaluation import *
from DSL import *

if __name__ == '__main__':
    # open Sparcraft as subprocess
    # game = Game(NOKDPS(0), AttackWeakest(1))
    # game.print_result()
    bound = 100
    use_triage = True
    eval_function = Evaluation()
    algorithm = ButtomUpSearch('', '')
    algorithm.search(
        bound,
        [Times, Plus, Minus, Argmax, Argmin, IT, ITE, LT, Equal, Sum, And, Or, Not, Map, Function],
        [-1, 0, 1, 2, 10],
        ['x', 'y', 'z'],
        ['num_attacks', 'num_moves', 'num_reload'],
        ['moves_distance', 'enemy_distance', 'enemy_hp', 'enemy_range', 'enemy_damage', 'enemy_dpf'],
        [],
        eval_function,
        use_triage
    )
