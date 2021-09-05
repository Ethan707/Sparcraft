'''
Author: Ethan Chen
Date: 2021-07-05 15:34:52
LastEditTime: 2021-09-05 15:39:07
LastEditors: Ethan Chen
Description: DSL for Sparcarft
FilePath: \Sparcraft\script\base_dsl.py
'''
import numpy as np
from GameState import *
import itertools


class Node:
    def __init__(self):
        self.size = 1
        self.max_limit = 0  # max amount
        self.current_child_amount = 0  # current amount
        self.children = []  # children list

        self.local = 'locals'
        self.intname = 'int'
        self.listname = 'list'
        self.tuplename = 'tuple'

    def add_child(self, child):
        if len(self.children) + 1 > self.max_limit:
            raise Exception('Unsupported number of children')

        self.children.append(child)
        self.current_child_amount += 1

        if child is None or not isinstance(child, Node):
            self.size += 1
        else:
            self.size += child.size

    def replace_child(self, child, index):
        if isinstance(self.children[index], Node):
            self.size -= self.children[index].size
        else:
            self.size -= 1

        if isinstance(child, Node):
            self.size += child.size
        else:
            self.size += 1

        self.children[index] = child

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def get_current_child_amount(self):
        return self.current_child_amount

    def get_max_limit(self):
        return self.max_limit

    def to_string(self):
        raise Exception('Unimplemented method: to_string')

    def interpret(self):
        raise Exception('Unimplemented method: interpret')

    def interpret_local_variables(self, env, x):
        if self.local not in env:
            env[self.local] = {}

        if type(x).__name__ == self.tuplename:
            x = list(x)

        env[self.local][type(x).__name__] = x

        return self.interpret(env)

    @classmethod
    def grow(plist):
        pass

    @classmethod
    def class_name(cls):
        return cls.__name__

    @staticmethod
    def factory(classname):
        if classname not in globals():
            return classname

        return globals()[classname]()

    @classmethod
    def accepted_initial_rules(cls):
        return cls.accepted_types

    @classmethod
    def accepted_rules(cls, child):
        return cls.accepted_types[child]


class Times(Node):
    def __init__(self):
        super(Times, self).__init__()
        self.max_limit = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)
        return inst

    def to_string(self):
        if len(self.children) < 2:
            raise Exception('Times: Incomplete Program')

        return "(" + self.children[0].to_string() + " * " + self.children[1].to_string() + ")"

    def interpret(self, env):
        if len(self.children) < 2:
            raise Exception('Times: Incomplete Program')

        return self.children[0].interpret(env) * self.children[1].interpret(env)

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


class Plus(Node):
    def __init__(self):
        super(Plus, self).__init__()
        self.max_limit = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def to_string(self):
        if len(self.children) < 2:
            raise Exception('Plus: Incomplete Program')
        return "(" + self.children[0].to_string() + " + " + self.children[1].to_string() + ")"

    def interpret(self, env):
        if len(self.children) < 2:
            raise Exception('Plus: Incomplete Program')
        return self.children[0].interpret(env) + self.children[1].interpret(env)

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


class Minus(Node):
    def __init__(self):
        super(Minus, self).__init__()
        self.max_limit = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)
        return inst

    def to_string(self):
        if len(self.children) < 2:
            raise Exception('Minus: Incomplete Program')
        return "(" + self.children[0].to_string() + " - " + self.children[1].to_string() + ")"

    def interpret(self, env):
        if len(self.children) < 2:
            raise Exception('Minus: Incomplete Program')
        return self.children[0].interpret(env) - self.children[1].interpret(env)

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


class Argmax(Node):
    def __init__(self):
        super(Argmax, self).__init__()
        self.max_limit = 1

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        return 'argmax(' + self.children[0].to_string() + ")"

    def interpret(self, env):
        return np.argmax(self.children[0].interpret(env))

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


class Argmin(Node):
    def __init__(self):
        super(Argmin, self).__init__()
        self.max_limit = 1

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        return 'argmin(' + self.children[0].to_string() + ")"

    def interpret(self, env):
        return np.argmin(self.children[0].interpret(env))

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


class IT(Node):
    def __init__(self):
        super(IT, self).__init__()
        self.max_limit = 2

    @classmethod
    def new(cls, if_arg, then_arg):
        inst = cls()
        inst.add_child(if_arg)
        inst.add_child(then_arg)
        return inst

    def to_string(self):
        if len(self.children) < 2:
            raise Exception('If then: Incomplete Program')
        return 'if ' + self.children[0].to_string() + ': \n\t' + self.children[1].to_string()

    def interpret(self, env):
        if len(self.children) < 2:
            raise Exception('If then: Incomplete Program')

        if self.children[0].interpret(env):
            return self.children[1].interpret(env)

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


class ITE(Node):
    def __init__(self):
        super(ITE, self).__init__()
        self.max_limit = 3

    @classmethod
    def new(cls, if_arg, then_arg, else_arg):
        inst = cls()
        inst.add_child(if_arg)
        inst.add_child(then_arg)
        inst.add_child(else_arg)
        return inst

    def to_string(self):
        if len(self.children) < 3:
            raise Exception('If then else: Incomplete Program')
        return 'if ' + self.children[0].to_string() + ': \n\t' + self.children[1].to_string() + '\n else: \n\t' + self.children[2].to_string()

    def interpret(self, env):
        if len(self.children) < 3:
            raise Exception('If then else: Incomplete Program')

        return self.children[1].interpret(env) if self.children[0].interpret(env) else self.children[2].interpret(env)

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


class LT(Node):
    def __init__(self):
        super(LT, self).__init__()
        self.max_limit = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def to_string(self):
        if len(self.children) < 2:
            raise Exception('less than: Incomplete Program')
        return self.children[0].to_string() + " < " + self.children[1].to_string()

    def interpret(self, env):
        if len(self.children) < 2:
            raise Exception('less than: Incomplete Program')
        return self.children[0].interpret(env) < self.children[1].interpret(env)

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


class Sum(Node):
    def __init__(self):
        super(Sum, self).__init__()
        self.max_limit = 1

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        return 'sum(' + self.children[0].to_string() + ")"

    def interpret(self, env):
        return np.sum(self.children[0].interpret(env))

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


class And(Node):
    def __init__(self):
        super(And, self).__init__()
        self.max_limit = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def to_string(self):
        if len(self.children) < 2:
            raise Exception('And: Incomplete Program')
        return "("+self.children[0].to_string() + " and " + self.children[1].to_string()+")"

    def interpret(self, env):
        if len(self.children) < 2:
            raise Exception('And: Incomplete Program')
        return self.children[0].interpret(env) and self.children[1].interpret(env)

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


class Or(Node):
    def __init__(self):
        super(Or, self).__init__()
        self.max_limit = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def to_string(self):
        if len(self.children) < 2:
            raise Exception('Or: Incomplete Program')
        return "("+self.children[0].to_string() + " or " + self.children[1].to_string()+")"

    def interpret(self, env):
        if len(self.children) < 2:
            raise Exception('Or: Incomplete Program')
        return self.children[0].interpret(env) or self.children[1].interpret(env)

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

# class Map(Node):
#     def __init__(self):
#         super(Map, self).__init__()

#         self.max_limit = 2

#     @classmethod
#     def new(cls, func, l):
#         inst = cls()
#         inst.add_child(func)
#         inst.add_child(l)

#         return inst

#     def to_string(self):
#         if self.children[1] is None:
#             return 'map(' + self.children[0].to_string() + ", None)"

#         return 'map(' + self.children[0].to_string() + ", " + self.children[1].to_string() + ")"

#     def interpret(self, env):
#         # if list is None, then it tries to retrieve from local variables from a lambda function
#         if self.children[1] is None:
#             list_var = env[self.local][self.listname]
#             return list(map(self.children[0].interpret(env), list_var))

#         return list(map(self.children[0].interpret(env), self.children[1].interpret(env)))


# class Function(Node):
#     def __init__(self):
#         super(Function, self).__init__()
#         self.max_limit = 1

#     @classmethod
#     def new(cls, var):
#         inst = cls()
#         inst.add_child(var)

#         return inst

#     def to_string(self):
#         return "(lambda x : " + self.children[0].to_string() + ")"

#     def interpret(self, env):
#         return lambda x: self.children[0].interpret_local_variables(env, x)


class StringConstant(Node):

    def __init__(self):
        super(StringConstant, self).__init__()
        self.max_limit = 1
        self.size = 0

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('String: Incomplete Program')

        return str(self.children[0])

    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('String: Incomplete Program')

        return self.children[0]


class NumericConstant(Node):

    def __init__(self):
        super(NumericConstant, self).__init__()
        self.max_limit = 1
        self.size = 0

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('Num: Incomplete Program')

        return str(self.children[0])

    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('Num: Incomplete Program')

        return self.children[0]


class VarList(Node):

    def __init__(self):
        super(VarList, self).__init__()
        self.max_limit = 1
        self.size = 0

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('VarList: Incomplete Program')

        return self.children[0]

    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('VarList: Incomplete Program')

        return env[self.children[0]]


class VarScalar(Node):

    def __init__(self):
        super(VarScalar, self).__init__()
        self.max_limit = 1
        self.size = 0

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('VarScalar: Incomplete Program')

        return self.children[0]

    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('VarScalar: Incomplete Program')

        return env[self.children[0]]


class ReturnPlayerAction(Node):
    def __init__(self):
        super(ReturnPlayerAction, self).__init__()
        self.max_limit = 1

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('return player action: Incomplete Program')

        return 'action_to_return = actions['+self.children[0].to_string()+']'

    def set_unit_state(self, env, unit: Unit):
        state = env['state']
        enemy = state.getEnemyFromUnit(unit)

        env['unit'] = unit
        env['moves_distance'] = unit.getMoveDistanceList()
        env['attack_actions'] = unit.getActionsByType(ATTACK)
        env['move_actions'] = unit.getActionsByType(MOVE)
        env['reload_actions'] = unit.getActionsByType(RELOAD)

        env['num_attacks'] = len(env['attack_actions'])
        env['num_moves'] = len(env['move_actions'])
        env['num_reload'] = len(env['reload_actions'])

        env['enemy_distance'] = state.getEnemyDistanceFromUnit(unit)
        env['enemy_hp'] = [i.hp for i in enemy]
        env['enemy_range'] = [i.range for i in enemy]
        env['enemy_damage'] = [i.damage for i in enemy]
        env['enemy_dpf'] = [i.dpf for i in enemy]

        env['unit_enemy'] = env['state'].getEnemyFromUnit(unit)
        env['global_enemy'] = env['state'].enemy_unit

    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('return player action: Incomplete Program')
        result = []
        units = env['state'].player_unit
        for unit in units:
            if len(unit.moves) > 0:
                self.set_unit_state(env, unit)
                index_unit_action = int(self.children[0].interpret(env))
                assert isinstance(index_unit_action, int) and 0 <= index_unit_action < len(unit.moves)
                result.append(index_unit_action)
        return result

    def grow(plist, size):
        new_programs = []

        program_set = plist.get_programs(size - 1)

        for t1, programs1 in program_set.items():
            # skip if t1 isn't a node accepted by Lt
            if t1 not in ReturnPlayerAction.accepted_rules(0):
                continue

            for p1 in programs1:

                assign = ReturnPlayerAction()
                assign.add_child(p1)
                new_programs.append(assign)

                yield assign
        return new_programs


class LTD_Score(Node):
    def __init__(self):
        super(LTD_Score, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        state = env['state']
        currentLTD = 0
        for unit in state.player_unit:
            currentLTD += unit.hp*unit.dpf

        return currentLTD


class LTD2_Score(Node):
    def __init__(self):
        super(LTD2_Score, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        state = env['state']
        currentLTD2 = 0
        for unit in state.player_unit:
            currentLTD2 += np.sqrt(unit.hp)*unit.dpf

        return currentLTD2


class LTD_PlayerOverOpponent(Node):
    def __init__(self):
        super(LTD_PlayerOverOpponent, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        state = env['state']
        playerLTD = 0
        enemyLTD = 0
        for unit in state.player_unit:
            playerLTD += unit.hp*unit.dpf
        for unit in state.enemy_unit:
            enemyLTD += unit.hp*unit.dpf
        return playerLTD-enemyLTD


class LTD2_PlayerOverOpponent(Node):
    def __init__(self):
        super(LTD2_PlayerOverOpponent, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        state = env['state']
        playerLTD2 = 0
        enemyLTD2 = 0
        for unit in state.player_unit:
            playerLTD2 += unit.hp*unit.dpf
        for unit in state.enemy_unit:
            enemyLTD2 += unit.hp*unit.dpf
        return playerLTD2-enemyLTD2


class HasAttackActions(Node):
    def __init__(self):
        super(HasAttackActions, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        unit = env['unit']
        num_actions = len(unit.getActionsByType(ATTACK))
        return num_actions > 0


class HasMoveActions(Node):
    def __init__(self):
        super(HasMoveActions, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        unit = env['unit']
        num_actions = len(unit.getActionsByType(MOVE))
        return num_actions > 0


class HasReloadActions(Node):
    def __init__(self):
        super(HasReloadActions, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        unit = env['unit']
        num_actions = len(unit.getActionsByType(RELOAD))
        return num_actions > 0


class AveDistancesFromMovePositionsToEnemyUnit(Node):
    def __init__(self):
        super(AveDistancesFromMovePositionsToEnemyUnit, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        moves = env['move_actions']
        global_enemy = env['global_enemy']

        distances = []
        for move in moves:
            tmp = 0
            for unit in global_enemy:
                position = [move[-2], move[-1]]
                tmp += unit.getDistanceToPosition(position)
            distances.append(tmp/len(global_enemy))

        return distances


class MinDistancesFromMovePositionsToEnemyUnit(Node):
    def __init__(self):
        super(MinDistancesFromMovePositionsToEnemyUnit, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        moves = env['move_actions']
        global_enemy = env['global_enemy']

        distances = []
        for move in moves:
            tmp = []
            for unit in global_enemy:
                position = [move[-2], move[-1]]
                tmp.append(unit.getDistanceToPosition(position))
            distances.append(min(tmp))
        return distances


class MaxDistancesFromMovePositionsToEnemyUnit(Node):
    def __init__(self):
        super(MaxDistancesFromMovePositionsToEnemyUnit, self).__init__()
        self.max_limit = 0

    def to_string(self):
        return type(self).__name__

    def interpret(self, env):
        moves = env['move_actions']
        global_enemy = env['global_enemy']

        distances = []
        for move in moves:
            tmp = []
            for unit in global_enemy:
                position = [move[-2], move[-1]]
                tmp.append(unit.getDistanceToPosition(position))
            distances.append(max(tmp))
        return distances


Times.accepted_nodes = set([VarScalar.class_name(),
                            NumericConstant.class_name(),
                            Plus.class_name(),
                            Times.class_name(),
                            Minus.class_name(),
                            Sum.class_name(), LTD2_PlayerOverOpponent.class_name(), LTD2_Score.class_name(
), LTD_PlayerOverOpponent.class_name(), LTD_Score.class_name()
])
Plus.accepted_nodes = set([VarScalar.class_name(),
                           NumericConstant.class_name(),
                           Plus.class_name(),
                           Times.class_name(),
                           Minus.class_name(),
                           Sum.class_name(), LTD2_PlayerOverOpponent.class_name(), LTD2_Score.class_name(
), LTD_PlayerOverOpponent.class_name(), LTD_Score.class_name()
])
Minus.accepted_nodes = set([VarScalar.class_name(),
                            NumericConstant.class_name(),
                            Plus.class_name(),
                            Times.class_name(),
                            Minus.class_name(),
                            Sum.class_name(), LTD2_PlayerOverOpponent.class_name(), LTD2_Score.class_name(
), LTD_PlayerOverOpponent.class_name(), LTD_Score.class_name()
])

Argmax.accepted_nodes = set([VarList.class_name(), AveDistancesFromMovePositionsToEnemyUnit.class_name(),
                             MinDistancesFromMovePositionsToEnemyUnit.class_name(), MaxDistancesFromMovePositionsToEnemyUnit.class_name()])
Argmin.accepted_nodes = set([VarList.class_name(), AveDistancesFromMovePositionsToEnemyUnit.class_name(),
                             MinDistancesFromMovePositionsToEnemyUnit.class_name(), MaxDistancesFromMovePositionsToEnemyUnit.class_name()])

ITE.accepted_nodes_bool = set([LT.class_name(),
                               And.class_name(), Or.class_name(), HasAttackActions.class_name(), HasMoveActions.class_name(), HasReloadActions.class_name()])
ITE.accepted_nodes_block = set([ITE.class_name(), IT.class_name(), Argmax.class_name(
), Argmin.class_name(), Times.class_name(), Plus.class_name(), Minus.class_name()])

IT.accepted_nodes_bool = set([LT.class_name(), And.class_name(), Or.class_name(
), HasAttackActions.class_name(), HasMoveActions.class_name(), HasReloadActions.class_name()])
IT.accepted_nodes_block = set([ITE.class_name(), IT.class_name(), Argmax.class_name(
), Argmin.class_name(), Times.class_name(), Plus.class_name(), Minus.class_name()])

LT.accepted_nodes = set([VarScalar.class_name(),
                         NumericConstant.class_name(),
                         Plus.class_name(),
                         Times.class_name(),
                         Minus.class_name(),
                         Sum.class_name(), LTD2_PlayerOverOpponent.class_name(), LTD2_Score.class_name(
), LTD_PlayerOverOpponent.class_name(), LTD_Score.class_name()])

Sum.accepted_nodes = set([VarList.class_name(), AveDistancesFromMovePositionsToEnemyUnit.class_name(),
                          MinDistancesFromMovePositionsToEnemyUnit.class_name(), MaxDistancesFromMovePositionsToEnemyUnit.class_name()])
And.accepted_nodes = set([LT.class_name(), HasAttackActions.class_name(),
                          HasMoveActions.class_name(), HasReloadActions.class_name()])
Or.accepted_nodes = set([LT.class_name(), HasAttackActions.class_name(),
                         HasMoveActions.class_name(), HasReloadActions.class_name()])
# Function.accepted_nodes = set([Minus.class_name(),
#                                Plus.class_name(),
#                                Times.class_name(),
#                                Sum.class_name(),
#                                Map.class_name()])
# Map.accepted_nodes_function = set([Function.class_name()])
# Map.accepted_nodes_list = set([VarList.class_name(), Map.class_name()])


Times.accepted_types = [Times.accepted_nodes, Times.accepted_nodes]
Plus.accepted_types = [Plus.accepted_nodes, Plus.accepted_nodes]
Minus.accepted_types = [Minus.accepted_nodes, Minus.accepted_nodes]
Argmax.accepted_types = [Argmax.accepted_nodes]
Argmin.accepted_types = [Argmin.accepted_nodes]
ITE.accepted_types = [ITE.accepted_nodes_bool, ITE.accepted_nodes_block, ITE.accepted_nodes_block]
IT.accepted_types = [IT.accepted_nodes_bool, IT.accepted_nodes_block]
LT.accepted_types = [LT.accepted_nodes, LT.accepted_nodes]
Sum.accepted_types = [Sum.accepted_nodes]
And.accepted_types = [And.accepted_nodes, And.accepted_nodes]
Or.accepted_types = [Or.accepted_nodes, Or.accepted_nodes]

ReturnPlayerAction.accepted_nodes = set([Argmax.class_name(), Argmin.class_name(), ITE.class_name(), IT.class_name(),
                                         NumericConstant.class_name(), Plus.class_name(), Minus.class_name(), Times.class_name()])
ReturnPlayerAction.accepted_types = [ReturnPlayerAction.accepted_nodes]
# Function.accepted_types = [Function.accepted_nodes]
# Map.accepted_types = [Map.accepted_nodes_function, Map.accepted_nodes_list]
Node.accepted_types = [set([ITE.class_name(), Argmax.class_name(), Argmin.class_name(),
                            Sum.class_name(), ReturnPlayerAction.class_name()])]
