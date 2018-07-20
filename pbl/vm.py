#!/usr/bin/env python
# coding: utf-8

from enum import Enum, unique

@unique
class Register(Enum):
    PC = 1
    SP = 2

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class VM(object):

    def __init__(self, stack_size=20):
        self.reg = {}
        self.stack = [0] * stack_size
        self.heap = []

        for r in Register:
            self.reg[r] = 0

    def __repr__(self):
        return str(self.__dict__)
