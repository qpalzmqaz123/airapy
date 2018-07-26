#!/usr/bin/env python
# coding: utf-8

from enum import Enum, unique

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
    # JMPT A: if S(-1) then R(PC) = A
    JMPT = 9
    # JMP A: R(PC) = A
    JMP = 10
    # EQ: S(-1) = S(-2) == S(-1)
    EQ = 11
    # GT: S(-1) = S(-2) > S(-1)
    GT = 12
    # GE: S(-1) = S(-2) >= S(-1)
    GE = 13
    # LT: S(-1) = S(-2) < S(-1)
    LT = 14
    # LE: S(-1) = S(-2) <= S(-1)
    LE = 15

class InstructionList(list):

    @property
    def lastIndex(self):
        return len(self) - 1

class Instruction(object):

    def __repr__(self):
        return '%-6s' % (type(self).__name__)

    def __str__(self):
        return self.__repr__()

class NOP(Instruction):

    def run(self, vm):
        vm.reg.PC += 1

class PUSH(Instruction):

    def __init__(self, source):
        self.source = source

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.source)

    def run(self, vm):
        vm.stack[vm.reg.SP] = self.source
        vm.reg.SP += 1
        vm.reg.PC += 1

class POP(Instruction):

    def run(self, vm):
        vm.reg.SP -= 1
        vm.reg.PC += 1

        return vm.stack[vm.reg.SP]

class MOV(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)

class ADD(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] + vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

class SUB(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)

class MUL(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] * vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

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
        vm.frame.hash[self.name] = vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

class GET(Instruction):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.name)

    def run(self, vm):
        vm.stack[vm.reg.SP] = vm.frame.hash[self.name]
        vm.reg.SP += 1
        vm.reg.PC += 1

class JMPT(Instruction):

    def __init__(self, index):
        self.index= index

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.index)

    def run(self, vm):
        if vm.stack[vm.reg.SP - 1]:
            vm.reg.PC = self.index
        else:
            vm.reg.PC += 1

        vm.reg.SP -= 1

class JMP(Instruction):

    def __init__(self, index):
        self.index= index

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.index)

    def run(self, vm):
        vm.reg.PC = self.index

class EQ(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] == vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

class GT(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] > vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

class GE(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] >= vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

class LT(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] < vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

class LE(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] <= vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1
