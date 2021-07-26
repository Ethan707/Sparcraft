'''
Author: Ethan Chen
Date: 2021-07-15 12:40:17
LastEditTime: 2021-07-26 07:28:46
LastEditors: Ethan Chen
Description: 
FilePath: /Sparcraft/script/main.py
'''
from Game import *
from BUS import *
from evaluation import *
from base_dsl import *
from simulated_annealing import *

if __name__ == '__main__':
    p = ReturnPlayerAction.new(
        Argmin.new(
            MaxDistancesFromMovePositionsToEnemyUnit()
        )
    )
    # open Sparcraft as subprocess
    # game = Game(NOKDPS(), AttackWeakest())
    # game.run_experiment()
    # game.print_result()

    # p = ReturnPlayerAction.new(
    #     ITE.new(
    #         HasAttackActions(),
    #         Argmin.new(VarList.new('enemy_hp')),
    #         ITE.new(
    #             HasMoveActions(),
    #             Argmin.new(MinDistancesFromMovePositionsToEnemyUnit()),
    #             NumericConstant.new(0)
    #         )
    #     ))
    # player = ProgramPlayer(p)
    # game = Game(player, AttackWeakestNOK(), num_exp=200)
    # game.run_experiment()
    # game.print_result()

    bound = 10
    use_triage = True
    eval_function = PlayWithRandomPlayer(10)
    # algorithm = ButtomUpSearch('', '')
    # algorithm.search(
    #     bound,
    #     [ReturnPlayerAction, Times, Plus, Minus, Argmax, Argmin, IT, ITE, LT, Sum],
    #     [0, 5, 50],
    #     ['y'],
    #     ['num_attacks', 'num_moves', 'num_reload'],
    #     ['moves_distance', 'enemy_distance', 'enemy_hp', 'enemy_range', 'enemy_damage', 'enemy_dpf'],
    #     [LTD_Score,
    #      LTD2_Score,
    #      LTD2_PlayerOverOpponent,
    #      LTD2_PlayerOverOpponent,
    #      HasAttackActions,
    #      HasMoveActions,
    #      HasReloadActions,
    #      AveDistancesFromMovePositionsToEnemyUnit,
    #      MinDistancesFromMovePositionsToEnemyUnit,
    #      MaxDistancesFromMovePositionsToEnemyUnit],
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
    algorithm.search([Times, Plus, Minus, Argmax, Argmin, IT, ITE, LT, Sum, ReturnPlayerAction],
                     [0, 5, 50],
                     ['y'],
                     ['num_attacks', 'num_moves', 'num_reload'],
                     ['moves_distance', 'enemy_distance', 'enemy_hp', 'enemy_range', 'enemy_damage', 'enemy_dpf'],
                     terminals,
                     eval_function,
                     use_triage,
                     float(100),
                     float(0.6),
                     float(100),
                     120000, initial_program=p)
