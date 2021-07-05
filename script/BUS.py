'''
Author: Ethan Chen
Date: 2021-07-05 16:30:54
LastEditTime: 2021-07-05 19:43:00
LastEditors: Ethan Chen
Description: Buttom up search for sparcraft
FilePath: \Sparcraft\script\BUS.py
'''


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

    def init_plist(self):
        pass

    def get_programs(self, size):
        if size in self.plist:
            return self.plist[size]
        return {}

    def get_number_programs(self):
        return self.number_program


class ButtomUpSearch():
    def __init__(self):
        pass

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

    def search(self, bound):
        self.closed_list = set()
        self.plist = ProgramList()
        self.plist.init_plist()

        current_size = 0

        # while current_size <= bound:
        # pass
        # TODO: operations
        # for p in self.grow(operations, current_size):
        #     pass
