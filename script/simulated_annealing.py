'''
Author: Ethan Chen
Date: 2021-07-22 04:32:29
LastEditTime: 2021-07-26 00:32:26
LastEditors: Ethan Chen
Description: 
FilePath: /Sparcraft/script/simulated_annealing.py
'''

from base_dsl import *

import numpy as np
import random
import time
from os.path import join
import os
import copy


class SimulatedAnnealing():

    def __init__(self, log_file, program_file):
        self.log_folder = 'logs/'
        self.program_folder = 'programs/'

        # if not os.path.exists(self.log_folder):
        #     os.makedirs(self.log_folder)

        # if not os.path.exists(self.program_folder):
        #     os.makedirs(self.program_folder)

        self.log_file = 'sa-' + log_file
        self.program_file = 'sa-' + program_file

    def mutate_inner_nodes_ast(self, p, index):
        self.processed += 1

        if not isinstance(p, Node):
            return False

        for i in range(p.get_max_limit()):

            if index == self.processed:
                # Accepted rules for the i-th child
                types = p.accepted_rules(i)

                # Generate instance of a random accepted rule
                child = Node.factory(list(types)[random.randrange(len(types))])

                # Randomly generate the child
                if isinstance(child, Node):
                    self.fill_random_program(child, 0, 4)

                # Replacing previous child with the randomly generated one
                p.replace_child(child, i)
                return True

            mutated = self.mutate_inner_nodes_ast(p.children[i], index)

            if mutated:

                # Fixing the size of all nodes in the AST along the modified branch
                modified_size = 1
                for j in range(p.get_max_limit()):
                    if isinstance(p.children[j], Node):
                        modified_size += p.children[j].get_size()
                    else:
                        modified_size += 1
                p.set_size(modified_size)

                return True

        return False

    def mutate(self, p):
        index = random.randrange(p.get_size())

        # Mutating the root of the AST
        if index == 0:
            initial_types = Node.accepted_rules(0)
            p = Node.factory(list(initial_types)[random.randrange(len(initial_types))])
            self.fill_random_program(p, 0, 4)

            return p

        self.processed = 0
        self.mutate_inner_nodes_ast(p, index)

        return p

    def return_terminal_child(self, p, types):
        terminal_types = []

        for t in types:
            child = p.factory(t)

            if child.get_max_limit() == 0 or isinstance(child, NumericConstant) or isinstance(child, StringConstant) or isinstance(child, VarList) or isinstance(child, VarScalar):
                terminal_types.append(child)

#         if len(terminal_types) == 0:
#             for t in types:
#                 child = p.factory(t)
#
#                 if child.get_max_limit() == 1:
#                     terminal_types.append(child)

        if len(terminal_types) > 0:
            return terminal_types[random.randrange(len(terminal_types))]

        return p.factory(list(types)[random.randrange(len(types))])

    def fill_random_program(self, p, depth, max_depth):

        size = p.get_size()

        for i in range(p.get_max_limit()):
            types = p.accepted_rules(i)

            if isinstance(p, NumericConstant) or isinstance(p, StringConstant) or isinstance(p, VarList) or isinstance(p, VarScalar):
                child = list(types)[random.randrange(len(types))]
                p.add_child(child)

                size += 1
            elif depth >= max_depth:
                child = self.return_terminal_child(p, types)
                p.add_child(child)
                child_size = self.fill_random_program(child, depth + 1, max_depth)

                size += child_size
            else:
                child = p.factory(list(types)[random.randrange(len(types))])
                p.add_child(child)
                child_size = self.fill_random_program(child, depth + 1, max_depth)

                size += child_size

        p.set_size(size)
        return size

    def random_program(self):

        initial_types = list(Node.accepted_initial_rules()[0])
        p = Node.factory(initial_types[random.randrange(len(initial_types))])

        self.fill_random_program(p, self.initial_depth_ast, self.max_mutation_depth)

        return p

    def accept_function(self, current_score, next_score):
        return np.exp(self.beta * (next_score - current_score)/self.current_temperature)

    def decrease_temperature(self, i):
        #         self.current_temperature = self.initial_temperature * self.alpha ** i
        self.current_temperature = self.initial_temperature / (1 + self.alpha * (i))

    def search(self,
               operations,
               numeric_constant_values,
               string_constant_values,
               variables_scalar,
               variables_list,
               functions_scalars,
               eval_function,
               use_triage,
               initial_temperature,
               alpha,
               beta,
               time_limit,
               winrate_target=None,
               initial_program=None):

        time_start = time.time()

        self.winrate_target = winrate_target

        self.max_mutation_depth = 4
        self.initial_depth_ast = 0
        self.initial_temperature = initial_temperature
        self.alpha = alpha
        self.beta = beta

        NumericConstant.accepted_types = [set(numeric_constant_values)]
        StringConstant.accepted_types = [set(string_constant_values)]
        VarList.accepted_types = [set(variables_list)]
        VarScalar.accepted_types = [set(variables_scalar)]
        # VarScalarFromArray.accepted_types = [set(variables_scalar_from_array)]

        self.operations = operations
        self.numeric_constant_values = numeric_constant_values
        self.string_constant_values = string_constant_values
        self.variables_list = variables_list
        # self.variables_scalar_from_array = variables_scalar_from_array
        self.functions_scalars = functions_scalars
        self.eval_function = eval_function

        best_score = 0.0
        best_program = None

        # id_log = 1
        number_games_played = 0

        if initial_program is not None:
            current_program = copy.deepcopy(initial_program)
        else:
            current_program = self.random_program()

        while True:
            self.current_temperature = self.initial_temperature

            if use_triage:
                current_score, _, number_matches_played = self.eval_function.eval_triage(current_program, best_score)
            else:
                current_score, _, number_matches_played = self.eval_function.eval(current_program)
            number_games_played += number_matches_played

            iteration_number = 1

            if self.winrate_target is not None and current_score >= self.winrate_target:
                return current_program, current_score

            if best_program is None or current_score > best_score:

                best_score = current_score
                best_program = current_program

            while self.current_temperature > 1:

                time_end = time.time()

                if time_end - time_start > time_limit - 60:
                    return best_score, best_program

                copy_program = copy.deepcopy(current_program)

                mutation = self.mutate(copy_program)
                print(mutation.to_string())
                if use_triage:
                    next_score, _, number_matches_played = self.eval_function.eval_triage(mutation, best_score)
                else:
                    next_score, _, number_matches_played = self.eval_function.eval(mutation)

                if self.winrate_target is not None and next_score >= self.winrate_target:
                    return mutation, next_score

                number_games_played += number_matches_played

                if best_program is None or next_score > best_score:

                    best_score = next_score
                    best_program = mutation

                prob_accept = min(1, self.accept_function(current_score, next_score))

                prob = random.uniform(0, 1)
                if prob < prob_accept:

                    current_program = mutation
                    current_score = next_score

                iteration_number += 1

                self.decrease_temperature(iteration_number)

            if initial_program is not None:
                current_program = copy.deepcopy(initial_program)
            else:
                current_program = self.random_program()

        return best_score, best_program
