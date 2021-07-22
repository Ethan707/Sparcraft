'''
Author: Ethan Chen
Date: 2021-07-22 20:00:58
LastEditTime: 2021-07-22 21:29:37
LastEditors: Ethan Chen
Description: 
FilePath: \Sparcraft\script\dsl_bus.py
'''
import base_dsl
import itertools
import numpy as np


class Times(base_dsl.Times):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue

            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in Times.accepted_rules(0):
                    continue

                for p1 in programs1:

                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in Times.accepted_rules(1):
                            continue

                        for p2 in programs2:

                            times = Times()
                            times.add_child(p1)
                            times.add_child(p2)
                            new_programs.append(times)

                            yield times
        return new_programs


class Plus(base_dsl.Plus):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue

            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in Plus.accepted_rules(0):
                    continue

                for p1 in programs1:

                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in Plus.accepted_rules(0):
                            continue

                        for p2 in programs2:

                            plus = Plus()
                            plus.add_child(p1)
                            plus.add_child(p2)
                            new_programs.append(plus)

                            yield plus
        return new_programs


class Minus(base_dsl.Minus):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue

            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in Minus.accepted_rules(0):
                    continue

                for p1 in programs1:

                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in Minus.accepted_rules(1):
                            continue

                        for p2 in programs2:

                            minus = Minus()
                            minus.add_child(p1)
                            minus.add_child(p2)
                            new_programs.append(minus)

                            yield minus
        return new_programs


class Argmax(base_dsl.Argmax):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []
        program_set = plist.get_programs(size - 1)

        for t1, programs1 in program_set.items():
            # skip if t1 isn't a node accepted by Lt
            if t1 not in Argmax.accepted_rules(0):
                continue

            for p1 in programs1:
                am = Argmax()
                am.add_child(p1)
                new_programs.append(am)

                yield am
        return new_programs


class Argmin(base_dsl.Argmin):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []
        program_set = plist.get_programs(size - 1)

        for t1, programs1 in program_set.items():
            # skip if t1 isn't a node accepted by Lt
            if t1 not in Argmin.accepted_rules(0):
                continue

            for p1 in programs1:

                am = Argmin()
                am.add_child(p1)
                new_programs.append(am)

                yield am
        return new_programs


class IT(base_dsl.IT):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue

            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
            for t1, programs1 in program_set1.items():
                if t1 not in IT.accepted_rules(0):
                    continue
                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        if t2 not in IT.accepted_rules(1):
                            continue
                        for p2 in programs2:
                            it = IT()
                            it.add_child(p1)
                            it.add_child(p2)
                            new_programs.append(it)
                            yield it
        return new_programs


class ITE(base_dsl.ITE):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=3))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + c[2] + 1 != size:
                continue

            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
            program_set3 = plist.get_programs(c[2])

            for t1, programs1 in program_set1.items():
                if t1 not in ITE.accepted_rules(0):
                    continue
                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        if t2 not in ITE.accepted_rules(1):
                            continue
                        for p2 in programs2:
                            for t3, programs3 in program_set3.items():
                                if t3 not in ITE.accepted_rules(2):
                                    continue
                                for p3 in programs3:
                                    ite = ITE()
                                    ite.add_child(p1)
                                    ite.add_child(p2)
                                    ite.add_child(p3)
                                    new_programs.append(ite)
                                    yield ite
        return new_programs


class LT(base_dsl.LT):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue

            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in LT.accepted_rules(0):
                    continue

                for p1 in programs1:

                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in LT.accepted_rules(1):
                            continue

                        for p2 in programs2:

                            lt = LT()
                            lt.add_child(p1)
                            lt.add_child(p2)
                            new_programs.append(lt)

                            yield lt
        return new_programs


class Sum(base_dsl.Sum):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        program_set = plist.get_programs(size - 1)

        for t1, programs1 in program_set.items():
            # skip if t1 isn't a node accepted by Lt
            if t1 not in Sum.accepted_rules(0):
                continue

            for p1 in programs1:

                sum_p = Sum()
                sum_p.add_child(p1)
                new_programs.append(sum_p)

                yield sum_p
        return new_programs


class And(base_dsl.And):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue

            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in And.accepted_rules(0):
                    continue

                for p1 in programs1:

                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in And.accepted_rules(1):
                            continue

                        for p2 in programs2:

                            lt = And()
                            lt.add_child(p1)
                            lt.add_child(p2)
                            new_programs.append(lt)

                            yield lt
        return new_programs


class Or(base_dsl.Or):
    def __init__(self):
        super().__init__()

    def grow(plist, size):
        new_programs = []

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue

            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in Or.accepted_rules(0):
                    continue

                for p1 in programs1:

                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in Or.accepted_rules(1):
                            continue

                        for p2 in programs2:

                            lt = Or()
                            lt.add_child(p1)
                            lt.add_child(p2)
                            new_programs.append(lt)

                            yield lt
        return new_programs


# class Map(base_dsl.Map):
#     def __init__(self):
#         super().__init__()

#     @staticmethod
#     def grow(plist, size):
#         new_programs = []

#         # generates all combinations of cost of size 2 varying from 1 to size - 1
#         combinations = list(itertools.product(range(0, size), repeat=2))

#         for c in combinations:
#             # skip if the cost combination exceeds the limit
#             if c[0] + c[1] + 1 != size:
#                 continue

#             # retrive bank of programs with costs c[0], c[1], and c[2]
#             program_set1 = plist.get_programs(c[0])
#             program_set2 = plist.get_programs(c[1])

#             for t1, programs1 in program_set1.items():
#                 # skip if t1 isn't a node accepted by Lt
#                 if t1 not in Map.accepted_rules(0):
#                     continue

#                 for p1 in programs1:

#                     for t2, programs2 in program_set2.items():

#                         # skip if t2 isn't a node accepted by Map
#                         if t2 not in Map.accepted_rules(1):
#                             continue

#                         for p2 in programs2:

#                             m = Map()
#                             m.add_child(p1)
#                             m.add_child(p2)
#                             new_programs.append(m)

#                             yield m
#         return new_programs


# class Function(base_dsl.Function):
#     def __init__(self):
#         super().__init__()

#     def grow(plist, size):
#         new_programs = []

#         program_set = plist.get_programs(size - 1)

#         for t1, programs1 in program_set.items():
#             # skip if t1 isn't a node accepted by Lt
#             if t1 not in Function.accepted_rules(0):
#                 continue

#             for p1 in programs1:

#                 func = Function()
#                 func.add_child(p1)
#                 new_programs.append(func)

#                 yield func
#         return new_programs


class StringConstant(base_dsl.StringConstant):

    def __init__(self):
        super().__init__()


class NumericConstant(base_dsl.NumericConstant):

    def __init__(self):
        super().__init__()


class VarList(base_dsl.VarList):

    def __init__(self):
        super().__init__()


class VarScalar(base_dsl.VarScalar):

    def __init__(self):
        super().__init__()


class ReturnPlayerAction(base_dsl.ReturnPlayerAction):
    def __init__(self):
        super().__init__()


class LTD_Score(base_dsl.LTD_Score):
    def __init__(self):
        super().__init__()


class LTD2_Score(base_dsl.LTD2_Score):
    def __init__(self):
        super().__init__()


class LTD_PlayerOverOpponent(base_dsl.LTD_PlayerOverOpponent):
    def __init__(self):
        super().__init__()


class LTD2_PlayerOverOpponent(base_dsl.LTD2_PlayerOverOpponent):
    def __init__(self):
        super().__init__()


class HasAttackActions(base_dsl.HasAttackActions):
    def __init__(self):
        super().__init__()


class HasMoveActions(base_dsl.HasMoveActions):
    def __init__(self):
        super().__init__()


class HasReloadActions(base_dsl.HasReloadActions):
    def __init__(self):
        super().__init__()


class AveDistancesFromMovePositionsToEnemyUnit(base_dsl.AveDistancesFromMovePositionsToEnemyUnit):
    def __init__(self):
        super().__init__()


class MinDistancesFromMovePositionsToEnemyUnit(base_dsl.MinDistancesFromMovePositionsToEnemyUnit):
    def __init__(self):
        super().__init__()


class MaxDistancesFromMovePositionsToEnemyUnit(base_dsl.MaxDistancesFromMovePositionsToEnemyUnit):
    def __init__(self):
        super().__init__()
