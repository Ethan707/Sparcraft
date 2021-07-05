'''
Author: Ethan Chen
Date: 2021-07-05 15:34:52
LastEditTime: 2021-07-05 19:20:01
LastEditors: Ethan Chen
Description: DSL for Sparcarft
FilePath: \Sparcraft\script\DSL.py
'''
import numpy as np


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


class IT(Node):
    def __init__(self):
        super(IT, self).__init__()
        self.max_limit = 2

    @classmethod
    def new(cls, if_arg, then_arg):
        # TODO:assert the if arg
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
