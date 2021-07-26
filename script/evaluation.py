'''
Author: Ethan Chen
Date: 2021-07-15 11:04:23
LastEditTime: 2021-07-26 05:58:59
LastEditors: Ethan Chen
Description: Evaluation function for BUS
FilePath: /Sparcraft/script/evaluation.py
'''

import os
# from Player_AttackClosest import AttackClosest
from Game import Game
from GameState import *
from Player_Random import RandomPlayer
from Player_AttackClosest import AttackClosest
from Player_AttackWeakest import AttackWeakest
from Program_Player import ProgramPlayer
from Player_NOKDPS import NOKDPS
from Player_AttackWeakestNOK import AttackWeakestNOK
from concurrent.futures.process import ProcessPoolExecutor


class Evaluation():

    number_matches_played = 0

    def __init__(self):
        # triage allows for programs that are 30% worse than the current best solution
        # in the first iteration and 20% worse solutions in the second iteration
        self.relative_slack_triage = [0.3, 0.2]

    def number_matches_triage(self, total_number_matches):
        first_layer = int(total_number_matches * 0.1)
        second_layer = int(total_number_matches * 0.4)
        third_layer = int(total_number_matches * 0.5)
        third_layer += total_number_matches - third_layer - second_layer - first_layer

        return [first_layer, second_layer, third_layer]

    def play_match(self, p1, p2, save_state_action_pairs=False):

        if save_state_action_pairs:
            self.state_action_pairs = []

        Evaluation.number_matches_played += 1

        game = Game(p1, p2)
        game.run_experiment()
        result = game.get_result()

        if result[0] > result[1]:
            return p1
        elif result[0] < result[1]:
            return p2
        return None

    def play_n_matches(self, n, p1, p2):

        br_victories = 0
        player_victories = 0

        Evaluation.number_matches_played = 0

        try:
            game = Game(p1, p2, num_exp=n)
            game.run_experiment()

            result = game.get_result()

            br_victories = result[1]
            player_victories = result[2]

        except Exception as e:
            print(e)
            return None, None, True

        return player_victories, br_victories, False

    @staticmethod
    def validate_parallel(data):
        index = data[0]
        program = data[1]

        game = GameState()
        path_name = '../game_record/'
        file_name = path_name+'record_'+str(index+1)+'.txt'
        try:
            with open(file_name) as f:
                lines = f.readlines()
                for line in lines:
                    message = line.split(' ')
                    if message[0] == 'PlayerID':
                        game.player_id = int(message[1])
                    elif message[0] == 'Time':
                        game.setTime(int(message[1]))
                    elif message[0] == 'Unit':
                        player = int(message[1])
                        hp = int(message[2])
                        firstTimeFree = int(message[3])
                        position = [int(message[4]), int(message[5])]
                        range = int(message[6])
                        damage = int(message[7])
                        dpf = float(message[8])
                        # set up the unit
                        unit = Unit(position, hp, range, damage, dpf)
                        # add unit to game state

                        if player == game.player_id:
                            game.addUnit(unit)
                        else:
                            game.addEnemy(unit)
                    elif message[0] == 'Move':
                        unitIndex = int(message[1])
                        player = int(message[2])

                        moveType = int(message[3])
                        moveIndex = int(message[4])
                        position_x = int(message[5])
                        position_y = int(message[6])
                        # set up the move
                        game.player_unit[unitIndex].moves.append([moveType, moveIndex, position_x, position_y])
                    elif message[0] == 'End':
                        decision = program.generate(game)
                        i = 0
                        for unit in game.player_unit:
                            if len(unit.moves) > 0:
                                assert decision[i] >= 0
                                assert decision[i] < len(unit.moves)
                                assert isinstance(decision[i], int)
                                i += 1
                        game.clear()
        except Exception:
            return True
        return False

    def validate_on_records(self, program):

        self.ncpus = int(os.environ.get('SLURM_CPUS_PER_TASK', default=4))

        try:
            with ProcessPoolExecutor(max_workers=self.ncpus) as executor:
                args = ((index, program) for index in range(20))
                results = executor.map(Evaluation.validate_parallel, args)
            for has_error in results:
                if has_error:
                    return True
        except Exception:
            return True

        return False

    def eval(self, br, player):

        _, br_victories, error = self.play_n_matches(self.number_evaluations, br, player)

        if error:
            return 0.0, error, self.number_evaluations

        return br_victories / self.number_evaluations, error, self.number_evaluations

    def eval_triage(self, br, player, current_best_score):

        number_matches_by_layer = self.number_matches_triage(self.number_evaluations)
        number_matches_played = 0

        br_victories = None
        error = None
        for i in range(20):
            data = [i, br]
            has_error = self.validate_parallel(data)
            if has_error:
                print("Error Validation")
                return 0.0, True, number_matches_played
            else:
                print("Pass")

        for i in range(len(number_matches_by_layer)):
            _, br_victories_local, error = self.play_n_matches(number_matches_by_layer[i], br, player)

            number_matches_played += number_matches_by_layer[i]

            if error:
                return 0.0, error, number_matches_played

            # print("Successful")
            if br_victories is None:
                br_victories = br_victories_local
            else:
                br_victories += br_victories_local

            if (i + 1) == len(number_matches_by_layer):
                return br_victories/number_matches_played, error, number_matches_played

            if br_victories / number_matches_played + (br_victories / number_matches_played) * self.relative_slack_triage[i] < current_best_score:
                return br_victories / number_matches_played, error, number_matches_played

        return br_victories / number_matches_played, error, number_matches_played


class PlayWithRandomPlayer(Evaluation):
    def __init__(self, number_evaluations):
        super(PlayWithRandomPlayer, self).__init__()
        self.number_evaluations = number_evaluations
        # self.player = RandomPlayer()
        self.player = AttackWeakestNOK()

    def eval(self, program):
        br = ProgramPlayer(program)
        return super().eval(br, self.player)

    def eval_triage(self, program, current_best_score):
        br = ProgramPlayer(program)
        return super().eval_triage(br, self.player, current_best_score)
