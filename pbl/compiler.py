#!/usr/bin/env python
# coding: utf-8

from enum import Enum, unique

@unique
class Register(Enum):
    R0 = 1
    R1 = 2
    R2 = 3

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

@unique
class Opcode(Enum):
    # NOP: no operation
    NOP = 0
    # MOV R(A) R(B): move R(A) to R(B)
    MOV = 1
    # LOADC A R(B): load const to register
    LOADC = 2
    # LOADM A R(B): load memory to register
    LOADM = 3
    # ADD R(A) R(B): R(A) = R(A) + R(B)
    ADD = 4
    # SUB R(A) R(B): R(A) = R(A) - R(B)
    SUB = 5
    # MUL R(A) R(B): R(A) = R(A) * R(B)
    MUL = 6
    # DIV R(A) R(B): R(A) = R(A) / R(B)
    DIV = 7
    # PUSH R(A): push R(A) to stack
    PUSH = 8
    # POP: pop top of stack to R(A)
    POP = 9

class Instruction(object):

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self.__dict__))

class NOP(Instruction):

    def __str__(self):
        return '%-6s' % (type(self).__name__)

class PUSH(Instruction):

    def __init__(self, source):
        self.source = source

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.source)

class POP(Instruction):

    def __init__(self, target):
        self.target = target

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.target)

class MOV(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)

class LOADC(Instruction):

    def __init__(self, value, target):
        self.value = value
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.value, self.target)

class LOADV(Instruction):

    def __init__(self):
        pass

class ADD(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)

class SUB(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)

class MUL(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)

class DIV(Instruction):

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return '%-6s %s %s' % (type(self).__name__, self.source, self.target)
