'''
Author: Ethan Chen
Date: 2021-07-15 11:04:23
LastEditTime: 2021-09-02 00:06:20
LastEditors: Ethan Chen
Description: Evaluation function for BUS
FilePath: \Sparcraft\script\evaluation.py
'''

import os
from Game import Game
from GameState import *
from Program_Player import ProgramPlayer
from concurrent.futures.process import ProcessPoolExecutor
from scripted_player import *


class Evaluation():

    number_matches_played = 0

    def __init__(self):
        # triage allows for programs that are 30% worse than the current best solution
        # in the first iteration and 20% worse solutions in the second iteration
        self.relative_slack_triage = [0.3, 0.2]

    def number_matches_triage(self, total_number_matches):
        '''triage setting for three layers [10% 40% 50%]'''
        first_layer = int(total_number_matches * 0.1)
        second_layer = int(total_number_matches * 0.4)
        third_layer = int(total_number_matches * 0.5)
        third_layer += total_number_matches - third_layer - second_layer - first_layer

        return [first_layer, second_layer, third_layer]

    def play_match(self, p1, p2, save_state_action_pairs=False):
        '''play one match with two given player
        return {has_finished, winner}
        '''

        if save_state_action_pairs:
            self.state_action_pairs = []

        Evaluation.number_matches_played += 1

        game = Game(p1, p2, num_exp=1)
        has_error = game.run_experiment()
        if has_error:
            return False, None
        result = game.get_result()  # result: [player1, player2, draw]

        if result[0] > result[1]:
            return True, p1
        elif result[0] < result[1]:
            return True, p2
        # the game will be draw if the players played too many steps
        # this had been set in the C++ file TODO
        # for example, player one only move to right and player two only move to left
        return False, None

    def play_n_matches(self, n, p1, p2):
        '''play n matches with two given players
            return {player_victories, br_victories, has_error}
        '''

        br_victories = 0
        player_victories = 0

        Evaluation.number_matches_played = 0

        game = Game(p1, p2, num_exp=n)
        has_error = game.run_experiment()

        if has_error:
            return None, None, True

        result = game.get_result()
        br_victories = result[1]
        player_victories = result[2]
        return player_victories, br_victories, False

    @staticmethod
    def validate_parallel(data):
        '''
            validate the program on game records,
            it is similar to the processGameState in Game.py

            return {has_error}
        '''
        index = data[0]  # index of the file [0...19]
        program = data[1]  # program needed to be validated

        path_name = '../game_record/'
        file_name = path_name+'record_'+str(index)+'.txt'
        try:
            with open(file_name) as f:
                game = GameState()
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
                        # if the game sate is end, generate decisions with the program
                        decision = program.generate(game)
                        i = 0  # the index of the decisions
                        for unit in game.player_unit:
                            # for each player, if it has avaliable moves, the program should return the move index with below rules
                            # 1. the move index is in [0...len(avaliable moves)]
                            # 2. it is an integer
                            if len(unit.moves) > 0:
                                assert decision[i] >= 0
                                assert decision[i] < len(unit.moves)
                                assert isinstance(decision[i], int)
                                i += 1
        except Exception:
            return True  # has error
        return False

    def validate_on_records(self, program):
        '''validate program parallely and return {has_error}'''

        self.ncpus = int(os.environ.get('SLURM_CPUS_PER_TASK', default=4))  # num of CPUs

        # parallel computation
        try:
            with ProcessPoolExecutor(max_workers=self.ncpus) as executor:
                args = ((index, program) for index in range(20))
                results = executor.map(Evaluation.validate_parallel, args)
            for has_error in results:
                # if has error, quit
                if has_error:
                    return True
        except Exception as e:
            print(e)
            return True

        return False

    def eval(self, br, player):
        '''
            basic evaluation function
            param {br}: the generated ProgramPlayer(program)
            param {player}: opponent
            return {winning_rate, has_error, number_evaluation}
        '''

        # if the program do not pass the validation on game records, quit
        has_error = self.validate_on_records(br)
        if has_error:
            print("Validation Error")
            return 0.0, has_error, self.number_evaluations
        print("Pass")

        # if the program pass the validation, go on real games
        _, br_victories, error = self.play_n_matches(self.number_evaluations, br, player)

        if error:
            return 0.0, error, self.number_evaluations

        return br_victories / self.number_evaluations, error, self.number_evaluations

    def eval_triage(self, br, player, current_best_score):
        '''
            basic triage evaluation function
            basic evaluation function
            param {br}: the generated ProgramPlayer(program)
            param {player}: opponent
            param {current_best_score}: current best winning rate
            return {winning_rate, has_error, number_evaluation}
        '''

        number_matches_by_layer = self.number_matches_triage(self.number_evaluations)
        number_matches_played = 0

        br_victories = None
        error = None
        # if the program do not pass the validation on game records, quit
        has_error = self.validate_on_records(br)
        if has_error:
            print("Validation Error")
            return 0.0, has_error, number_matches_played
        print("Pass")

        # run the evaluation for each layer in the triage
        for i in range(len(number_matches_by_layer)):
            _, br_victories_local, error = self.play_n_matches(number_matches_by_layer[i], br, player)

            number_matches_played += number_matches_by_layer[i]

            if error:
                return 0.0, error, number_matches_played

            if br_victories is None:
                br_victories = br_victories_local
            else:
                br_victories += br_victories_local

            if (i + 1) == len(number_matches_by_layer):
                return br_victories/number_matches_played, error, number_matches_played

            if br_victories / number_matches_played + (br_victories / number_matches_played) * self.relative_slack_triage[i] < current_best_score:
                return br_victories / number_matches_played, error, number_matches_played

        return br_victories / number_matches_played, error, number_matches_played


class EvalProgramDefeatsStrategy(Evaluation):
    '''
        Evaluate the program with given player
        Default player: AttackClosest
    '''

    def __init__(self, number_evaluations, player=AttackClosest()):
        super(EvalProgramDefeatsStrategy, self).__init__()
        self.number_evaluations = number_evaluations
        self.player = player

    def eval(self, program):
        br = ProgramPlayer(program)
        return super().eval(br, self.player)

    def eval_triage(self, program, current_best_score):
        br = ProgramPlayer(program)
        return super().eval_triage(br, self.player, current_best_score)
