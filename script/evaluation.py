'''
Author: Ethan Chen
Date: 2021-07-15 11:04:23
LastEditTime: 2021-07-17 00:03:50
LastEditors: Ethan Chen
Description: Evaluation function for BUS
FilePath: \Sparcraft\script\evaluation.py
'''

import os
from concurrent.futures.process import ProcessPoolExecutor
from Game import Game


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

    @staticmethod
    def play_match_parallel(data):
        p1 = data[0]
        p2 = data[1]

        Evaluation.number_matches_played += 1

        game = Game(p1, p2)
        game.init_experiment()
        game.run_experiment()
        result = game.get_result()

        if result[0] > result[1]:
            return True, 1, p1, p2
        elif result[0] < result[1]:
            return True, 2, p1, p2
        elif result[0] == result[1]:
            if result[1] == 0 and result[2] > 0:
                return False, None, p1, p2
            return True, None, p1, p2
        # have ever won?; program

    def play_match(self, p1, p2, save_state_action_pairs=False):

        if save_state_action_pairs:
            self.state_action_pairs = []

        Evaluation.number_matches_played += 1

        game = Game(p1, p2)
        game.init_experiment()
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
            game = Game(p1, p2, '')
        except Exception:
            return None, None, True

        return player_victories, br_victories, False

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
