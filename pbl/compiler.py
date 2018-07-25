#!/usr/bin/env python
# coding: utf-8

from enum import Enum, unique
from .vm import Register

@unique
class Opcode(Enum):
    # NOP: no operation
    NOP = 0
    # PUSH A: S(-1) = A
    PUSH = 1
    # POP: pop S(-1)
    POP = 2
    # ADD: S(-2) = S(-2) + S(-1)
    ADD = 3
    # SUB: S(-2) = S(-2) - S(-1)
    SUB = 4
    # MUL: S(-2) = S(-2) * S(-1)
    MUL = 5
    # DIV: S(-2) = S(-2) / S(-1)
    DIV = 6
    # SET A: HASH(A) = S(-1)
    SET = 7
    # GET A: S(-1) = HASH(A)
    GET = 8

class Instruction(object):

    def __repr__(self):
        return '%-6s' % (type(self).__name__)

    def __str__(self):
        return self.__repr__()

class NOP(Instruction):

    def run(self, vm):
        vm.reg[Register.PC] += 1

class PUSH(Instruction):

    def __init__(self, source):
        self.source = source

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.source)

    def run(self, vm):
        vm.stack[vm.reg[Register.SP]] = self.source
        vm.reg[Register.SP] += 1
        vm.reg[Register.PC] += 1

class POP(Instruction):

    def run(self, vm):
        vm.reg[Register.SP] -= 1
        vm.reg[Register.PC] += 1

        return vm.stack[vm.reg[Register.SP]]

class MOV(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)

class ADD(Instruction):

    def run(self, vm):
        vm.stack[vm.reg[Register.SP] - 2] = vm.stack[vm.reg[Register.SP] - 2] + vm.stack[vm.reg[Register.SP] - 1]
        vm.reg[Register.SP] -= 1
        vm.reg[Register.PC] += 1

class SUB(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)

class MUL(Instruction):

    def run(self, vm):
        vm.stack[vm.reg[Register.SP] - 2] = vm.stack[vm.reg[Register.SP] - 2] * vm.stack[vm.reg[Register.SP] - 1]
        vm.reg[Register.SP] -= 1
        vm.reg[Register.PC] += 1

class DIV(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)

class SET(Instruction):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.name)

    def run(self, vm):
        vm.frame.hash[self.name] = vm.stack[vm.reg[Register.SP] - 1]
        vm.reg[Register.SP] -= 1
        vm.reg[Register.PC] += 1

class GET(Instruction):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.name)

    def run(self, vm):
        vm.stack[vm.reg[Register.SP]] = vm.frame.hash[self.name]
        vm.reg[Register.SP] += 1
        vm.reg[Register.PC] += 1
