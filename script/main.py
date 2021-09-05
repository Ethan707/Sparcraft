from Game import *
from BUS import *
from evaluation import *
from base_dsl import *
from simulated_annealing import *
# import faulthandler # fault handler library import
import numpy as np
import argparse


if __name__ == '__main__':
    # the fault handler to trace the error
    # faulthandler.enable()
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

    parser = argparse.ArgumentParser()

    parser.add_argument('-search', action='store', dest='search_algorithm',
                        default='BottomUpSearch',
                        help='Search Algorithm (SimulatedAnnealing, BottomUpSearch)')

    parser.add_argument('-bound', action='store', dest='bound', default=20,
                        help='Bound for Bottom-Up Search')

    parser.add_argument('-e', action='store', dest='eval_function',
                        default='EvalProgramDefeatsStrategy',
                        help='Evaluation function')

    parser.add_argument('-n', action='store', dest='number_games', default=10,
                        help='Number of games played in each evaluation')

    parser.add_argument('-time', action='store', dest='time_limit', default=120,
                        help='Time limit in seconds')

    parser.add_argument('-temperature', action='store', dest='initial_temperature', default=100,
                        help='SA\'s initial temperature')

    parser.add_argument('-alpha', action='store', dest='alpha', default=0.6,
                        help='SA\'s alpha value')

    parser.add_argument('-beta', action='store', dest='beta', default=100,
                        help='SA\'s beta value')

    parser.add_argument('-log_file', action='store', dest='log_file',
                        help='File in which results will be saved')

    parser.add_argument('-program_file', action='store', dest='program_file',
                        help='File in which programs will be saved')

    parser.add_argument('--detect-equivalence', action='store_true', default=False,
                        dest='detect_equivalence',
                        help='Detect observational equivalence in Bottom-Up Search.')

    parser.add_argument('--triage_eval', action='store_true', default=False,
                        dest='use_triage',
                        help='Use a 3-layer triage for evaluating programs.')

    parser.add_argument('--triage_valid', action='store_true', default=False,
                        dest='use_triage',
                        help='Use a 3-layer triage for validation set.')

    parameters = parser.parse_args()

    number_games = int(parameters.number_games)  # amount of games for evaluating the program
    eval_function = globals()[parameters.eval_function](number_games)  # evaluation method

    time_limit = int(parameters.time_limit)  # time limit for searching
    algorithm = globals()[parameters.search_algorithm](parameters.log_file, parameters.program_file)

    if isinstance(algorithm, BottomUpSearch):
        algorithm.search(
            int(parameters.bound),
            [ReturnPlayerAction, Times, Plus, Minus, Argmax, Argmin, IT, ITE, LT, Sum],
            [0, 5, 50],
            ['y'],
            ['num_attacks', 'num_moves', 'num_reload'],
            ['moves_distance', 'enemy_distance', 'enemy_hp', 'enemy_range', 'enemy_damage', 'enemy_dpf'],
            [LTD_Score,
             LTD2_Score,
             LTD2_PlayerOverOpponent,
             LTD2_PlayerOverOpponent,
             HasAttackActions,
             HasMoveActions,
             HasReloadActions,
             AveDistancesFromMovePositionsToEnemyUnit,
             MinDistancesFromMovePositionsToEnemyUnit,
             MaxDistancesFromMovePositionsToEnemyUnit],
            eval_function,
            parameters.use_triage,
            time_limit
        )
    if isinstance(algorithm, SimulatedAnnealing):
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
                         parameters.use_triage,
                         float(100),
                         float(0.6),
                         float(100),
                         120000)
