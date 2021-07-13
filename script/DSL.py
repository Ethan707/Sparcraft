'''
Author: Ethan Chen
Date: 2021-07-05 15:34:52
LastEditTime: 2021-07-13 22:02:30
LastEditors: Ethan Chen
Description: DSL for Sparcarft
FilePath: \Sparcraft\script\DSL.py
'''
import numpy as np
import itertools


class Node:
    def __init__(self):
        self.size = 1
        self.max_limit = 0  # max amount
        self.current_child_amount = 0  # current amount
        self.children = []

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

    @classmethod
    def grow(plist):
        pass

    @classmethod
    def class_name(cls):
        return cls.__name__


class Constant(Node):

    def __init__(self):
        super(Constant, self).__init__()
        self.max_limit = 1
        self.size = 0

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)
        return inst

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('Constant: Incomplete Program')

        return str(self.children[0])

    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('Constant: Incomplete Program')
        return self.children[0]


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
                            times.addChild(p1)
                            times.addChild(p2)
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
                            plus.addChild(p1)
                            plus.addChild(p2)
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
                            minus.addChild(p1)
                            minus.addChild(p2)
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
                am.addChild(p1)
                new_programs.append(am)

                yield am
        return new_programs


class Argmin(Node):
    def __init__(self):
        super(Argmax, self).__init__()
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
                am.addChild(p1)
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
                            it.addChild(p1)
                            it.addChild(p2)
                            new_programs.append(it)
                            yield it
        return new_programs


class ITE(Node):
    def __init__(self):
        super(ITE, self).__init__()
        self.max_limit = 3

    @classmethod
    def new(cls, if_arg, then_arg, else_arg):
        # TODO:assert the if arg
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
                                    ite.addChild(p1)
                                    ite.addChild(p2)
                                    ite.addChild(p3)
                                    new_programs.append(ite)
                                    yield ite
        return new_programs


class LT(Node):
    def __init__(self):
        super(LT, self).__init__()
        self.number_children = 2

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
                            lt.addChild(p1)
                            lt.addChild(p2)
                            new_programs.append(lt)

                            yield lt
        return new_programs


class Equal(Node):
    def __init__(self):
        super(Equal, self).__init__()
        self.number_children = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def to_string(self):
        if len(self.children) < 2:
            raise Exception('less than: Incomplete Program')
        return self.children[0].to_string() + " == " + self.children[1].to_string()

    def interpret(self, env):
        if len(self.children) < 2:
            raise Exception('less than: Incomplete Program')
        return self.children[0].interpret(env) == self.children[1].interpret(env)

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
                if t1 not in Equal.accepted_rules(0):
                    continue

                for p1 in programs1:

                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in Equal.accepted_rules(1):
                            continue

                        for p2 in programs2:

                            lt = Equal()
                            lt.addChild(p1)
                            lt.addChild(p2)
                            new_programs.append(lt)

                            yield lt
        return new_programs


class Sum(Node):
    def __init__(self):
        super(Sum, self).__init__()
        self.number_children = 1

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
                sum_p.addChild(p1)
                new_programs.append(sum_p)

                yield sum_p
        return new_programs


class VarList(Node):

    def __init__(self):
        super(VarList, self).__init__()
        self.number_children = 1
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


class AssignActionToReturn(Node):
    def __init__(self):
        super(AssignActionToReturn, self).__init__()
        self.number_children = 1

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('AssignActionToReturn: Incomplete Program')

        return 'action_to_return = actions[' + self.children[0].to_string() + ']'

    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('AssignActionToReturn: Incomplete Program')

        env['action_to_return'] = env['actions'][self.children[0].interpret(env)]


class And(Node):
    def __init__(self):
        super(And, self).__init__()
        self.number_children = 2

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
                            lt.addChild(p1)
                            lt.addChild(p2)
                            new_programs.append(lt)

                            yield lt
        return new_programs


class Or(Node):
    def __init__(self):
        super(Or, self).__init__()
        self.number_children = 2

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
                            lt.addChild(p1)
                            lt.addChild(p2)
                            new_programs.append(lt)

                            yield lt
        return new_programs


class Not(Node):
    def __init__(self):
        super(Not, self).__init__()
        self.number_children = 1

    @classmethod
    def new(cls, left):
        inst = cls()
        inst.add_child(left)

        return inst

    def to_string(self):
        if len(self.children) < 1:
            raise Exception('Not: Incomplete Program')
        return "not "+self.children[0].to_string()

    def interpret(self, env):
        if len(self.children) < 1:
            raise Exception('Not: Incomplete Program')
        return not self.children[0].interpret(env)

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        program_set = plist.get_programs(size - 1)

        for t1, programs1 in program_set.items():
            # skip if t1 isn't a node accepted by Lt
            if t1 not in Not.accepted_rules(0):
                continue

            for p1 in programs1:

                sum_p = Not()
                sum_p.addChild(p1)
                new_programs.append(sum_p)

                yield sum_p
        return new_programs


class Map(Node):
    def __init__(self):
        super(Map, self).__init__()

        self.number_children = 2

    @classmethod
    def new(cls, func, l):
        inst = cls()
        inst.add_child(func)
        inst.add_child(l)

        return inst

    def to_string(self):
        if self.children[1] is None:
            return 'map(' + self.children[0].to_string() + ", None)"

        return 'map(' + self.children[0].to_string() + ", " + self.children[1].to_string() + ")"

    def interpret(self, env):
        # TODO: modify
        # if list is None, then it tries to retrieve from local variables from a lambda function
        if self.children[1] is None:
            list_var = env[self.local][self.listname]
            return list(map(self.children[0].interpret(env), list_var))

        return list(map(self.children[0].interpret(env), self.children[1].interpret(env)))


class Function(Node):
    def __init__(self):
        super(Function, self).__init__()
        self.number_children = 1

    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)

        return inst

    def to_string(self):
        return "(lambda x : " + self.children[0].to_string() + ")"

    def interpret(self, env):
        return lambda x: self.children[0].interpret_local_variables(env, x)

# TODO:
# len
