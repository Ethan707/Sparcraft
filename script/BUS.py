'''
Author: Ethan Chen
Date: 2021-07-05 16:30:54
LastEditTime: 2021-07-22 22:16:05
LastEditors: Ethan Chen
Description: Buttom up search for sparcraft
FilePath: \Sparcraft\script\BUS.py
'''

from Constant import ATTACK, MOVE, RELOAD
from GameState import GameState, Unit
from base_dsl import *
from evaluation import Evaluation


class ProgramList():
    def __init__(self):
        self.plist = {}
        self.number_program = 0

    def insert(self, program):
        if program.get_size() not in self.plist:
            self.plist[program.get_size()] = {}

        if program.class_name() not in self.plist[program.get_size()]:
            self.plist[program.get_size()][program.class_name()] = []

        self.plist[program.get_size()][program.class_name()].append(program)
        self.number_program += 1

    def get_programs(self, size):
        if size in self.plist:
            return self.plist[size]
        return {}

    def get_number_programs(self):
        return self.number_program


class ButtomUpSearch():

    def __init__(self, log_file, program_file, log_results=True):
        self.log_results = log_results

        if self.log_results:
            self.log_folder = 'logs/'
            self.program_folder = 'programs/'

            self.log_file = 'bus-' + log_file
            self.program_file = 'bus-' + program_file

    def generate_initial_set_of_programs(self, numeric_constant_values,
                                         string_constant_values,
                                         variables_scalar,
                                         variables_list,
                                         functions_scalars):
        set_of_initial_programs = []

        for i in variables_scalar:
            p = VarScalar.new(i)

            # if self.detect_equivalence and self.has_equivalent(p):
            #     continue

            set_of_initial_programs.append(p)

        for i in variables_list:
            p = VarList.new(i)

            # if self.detect_equivalence and self.has_equivalent(p):
            #     continue

            set_of_initial_programs.append(p)

        for i in numeric_constant_values:
            constant = NumericConstant.new(i)

            # if self.detect_equivalence and self.has_equivalent(constant):
            #     continue

            set_of_initial_programs.append(constant)

        for i in string_constant_values:
            constant = StringConstant.new(i)

            # if self.detect_equivalence and self.has_equivalent(constant):
            #     continue

            set_of_initial_programs.append(constant)

        for i in functions_scalars:
            p = i()

            # if self.detect_equivalence and self.has_equivalent(p):
            #     continue

            set_of_initial_programs.append(p)

        return set_of_initial_programs

    def grow(self, operations, size):
        new_programs = []
        for op in operations:
            for p in op.grow(self.plist, size):
                if p.to_string() not in self.closed_list:
                    self.closed_list.add(p.to_string())
                    new_programs.append(p)
                    yield p

        for p in new_programs:
            self.plist.insert(p)

    def get_closed_list(self):
        return self.closed_list

    def search(self,
               bound,
               operations,
               numeric_constant_values,
               string_constant_values,
               variables_scalar,
               variables_list,
               functions_scalars,
               eval_function: Evaluation,
               use_triage,
               collect_library=False):

        NumericConstant.accepted_types = [set(numeric_constant_values)]
        StringConstant.accepted_types = [set(string_constant_values)]
        VarList.accepted_types = [set(variables_list)]
        VarScalar.accepted_types = [set(variables_scalar)]
        # VarScalarFromArray.accepted_types = [set(variables_scalar_from_array)]

        self.closed_list = set()
        self.programs_outputs = set()

        initial_set_of_programs = self.generate_initial_set_of_programs(numeric_constant_values,
                                                                        string_constant_values,
                                                                        variables_scalar,
                                                                        variables_list,
                                                                        functions_scalars)
        self.plist = ProgramList()
        for p in initial_set_of_programs:
            self.plist.insert(p)

        number_programs_evaluated = 0
        number_games_played = 0
        current_size = 0

        best_winrate = 0.0
        best_program = None

        while current_size <= bound:

            number_evaluations_bound = 0

            for p in self.grow(operations, current_size):
                number_programs_evaluated += 1
                number_evaluations_bound += 1
                print(p.to_string())
                if type(p) != ReturnPlayerAction:
                    print("Yes")
                    if collect_library:
                        score = 0
                    else:
                        if use_triage:
                            score, _, number_matches_played = eval_function.eval_triage(p, best_winrate)
                            if score > 0:
                                print(score, number_matches_played)
                        else:
                            score, _, number_matches_played = eval_function.eval(p)
                        number_games_played += number_matches_played

                    if best_program is None or score > best_winrate:
                        best_winrate = score
                        best_program = p
                        print("Found")
                        print(p.to_string())

                current_size += 1

            if collect_library:
                return self.plist.plist

        return best_winrate, best_program, number_programs_evaluated, number_games_played
