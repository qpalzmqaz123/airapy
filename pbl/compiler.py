#!/usr/bin/env python
# coding: utf-8

from enum import Enum, unique
from .vm import Frame
from . import object as obj

@unique
class Opcode(Enum):
    # NOP: no operation
    NOP = 0
    # PUSH A: S(-1) = A
    PUSH = 1
    # PUSHL A: frame.loop.append((R(PC) + 1, A))
    PUSHL = 103
    # POP: pop S(-1)
    POP = 2
    # POPN: pop S(-1) ... S(-n)
    POPN = 101
    # POPL: frame.loop.pop()
    POPL = 104
    # CONT: R(PC) = frame.loop[-1]
    CONT = 105
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
    # PSET A: parent HASH(A) = S(-1)
    PSET = 106
    # GET A: S(-1) = HASH(A)
    GET = 8
    # JMPT A: if S(-1) then R(PC) = A
    JMPT = 9
    # JMPF A: if not S(-1) then R(PC) = A
    JMPF = 10
    # JMP A: R(PC) = A
    JMP = 11
    # EQ: S(-1) = S(-2) == S(-1)
    EQ = 12
    # NE: S(-1) = S(-2) != S(-1)
    NE = 102
    # GT: S(-1) = S(-2) > S(-1)
    GT = 13
    # GE: S(-1) = S(-2) >= S(-1)
    GE = 14
    # LT: S(-1) = S(-2) < S(-1)
    LT = 15
    # LE: S(-1) = S(-2) <= S(-1)
    LE = 16
    # AND: S(-1) = S(-2) and S(-1)
    AND = 107
    # OR: S(-1) = S(-2) OR S(-1)
    OR = 108
    # NOT: S(-1) = not S(-1)
    NOT = 109
    # RET: return S(-1)
    RET = 17
    # DUP A: duplicate S(A) -> S(-1)
    DUP = 18
    # MKFN A:
    MKFN = 19
    # CALL: R(PC) = S(-1) then create a new frame
    CALL = 20
    # MKARR A: S(-A) = [S(-A) ... S(-1)]
    MKARR = 21
    # SETP: HASH(S(-3))[S(-2)] = S(-1)
    SETP = 23
    # GETP: S(-2) = S(-2)[S(-1)]
    GETP = 24

class InstructionList(list):

    @property
    def lastIndex(self):
        return len(self) - 1

class Instruction(object):

    def __repr__(self):
        return '%-6s' % (type(self).__name__)

    def __str__(self):
        return self.__repr__()

    def run(self, vm):
        vm.reg.PC += 1

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

class POPN(Instruction):

    def __init__(self, number):
        if number <= 0:
            raise Exception('Invliad number')

        self.number = number

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.number)

    def run(self, vm):
        vm.reg.SP -= self.number
        vm.reg.PC += 1

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

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] - vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

class MUL(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] * vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

class DIV(Instruction):

    def run(self, vm):
        if type(vm.stack[vm.reg.SP - 2]) == float or type(vm.stack[vm.reg.SP - 1]) == float:
            vm.stack[vm.reg.SP - 2] = float(vm.stack[vm.reg.SP - 2] / vm.stack[vm.reg.SP - 1])
        else:
            vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] // vm.stack[vm.reg.SP - 1]
        vm.reg.SP -= 1
        vm.reg.PC += 1

class SET(Instruction):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.name)

    def run(self, vm):
        vm.frame.hash[self.name] = vm.stack[vm.reg.SP - 1]
        vm.reg.PC += 1

class PSET(Instruction):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.name)

    def run(self, vm):
        self._set(vm.frame, self.name, vm.stack[vm.reg.SP - 1])
        vm.reg.PC += 1

    def _set(self, frame, key, value):
        if key in frame.hash:
            frame.hash[key] = value
        elif frame.parent:
            return self._set(frame.parent, key, value)
        else:
            raise Exception("'%s' is not defined" % key)

class GET(Instruction):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.name)

    def run(self, vm):
        vm.stack[vm.reg.SP] = self._get(vm.frame, self.name)
        vm.reg.SP += 1
        vm.reg.PC += 1

    def _get(self, frame, key):
        if key in frame.hash:
            return frame.hash[key]
        elif frame.parent:
            return self._get(frame.parent, key)
        else:
            raise Exception("'%s' is not defined" % key)

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

class JMPF(Instruction):

    def __init__(self, index):
        self.index= index

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.index)

    def run(self, vm):
        if not vm.stack[vm.reg.SP - 1]:
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

class NE(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = vm.stack[vm.reg.SP - 2] != vm.stack[vm.reg.SP - 1]
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

class AND(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = bool(vm.stack[vm.reg.SP - 2] and vm.stack[vm.reg.SP - 1])
        vm.reg.SP -= 1
        vm.reg.PC += 1

class OR(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 2] = bool(vm.stack[vm.reg.SP - 2] or vm.stack[vm.reg.SP - 1])
        vm.reg.SP -= 1
        vm.reg.PC += 1

class NOT(Instruction):

    def run(self, vm):
        vm.stack[vm.reg.SP - 1] = bool(not vm.stack[vm.reg.SP - 1])
        vm.reg.PC += 1

class RET(Instruction):

    def run(self, vm):
        ret_val = vm.stack[vm.reg.SP - 1]

        vm.pop_frame()

        vm.reg.PC += 1
        vm.stack[vm.reg.SP - 1] = ret_val

class DUP(Instruction):

    def __init__(self, index):
        if index > -1:
            raise Exception('Invliad index')

        self.index = index

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.index)

    def run(self, vm):
        vm.stack[vm.reg.SP] = vm.stack[vm.reg.SP + self.index]
        vm.reg.SP += 1
        vm.reg.PC += 1

class MKFN(Instruction):

    def __init__(self, index):
        self.index = index

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.index)

    def run(self, vm):
        vm.stack[vm.reg.SP] = obj.Function(self.index, vm.frame)
        vm.reg.SP += 1
        vm.reg.PC += 1

class CALL(Instruction):

    def run(self, vm):
        fn = vm.stack[vm.reg.SP - 1]

        frame = Frame(fn.parent_frame)
        vm.push_frame(frame)

        vm.reg.PC = fn.index

class PUSHL(Instruction):

    def __init__(self, index):
        self.index = index

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.index)

    def run(self, vm):
        vm.reg.PC += 1

        vm.frame.loop.append((vm.reg.PC, self.index))

class POPL(Instruction):

    def run(self, vm):
        (pc, index) = vm.frame.loop.pop()

        vm.reg.PC = index + 1

class CONT(Instruction):

    def run(self, vm):
        (pc, index) = vm.frame.loop[-1]

        vm.reg.PC = pc

class MKARR(Instruction):

    def __init__(self, cnt):
        self.cnt = cnt

    def __str__(self):
        return '%-6s %s' % (type(self).__name__, self.cnt)

    def run(self, vm):
        vm.reg.PC += 1

        arr = obj.Array()
        for i in range(self.cnt):
            arr.append(vm.stack[vm.reg.SP - self.cnt + i])

        vm.stack[vm.reg.SP - self.cnt] = arr
        vm.reg.SP -= self.cnt - 1

class SETP(Instruction):
    pass

class GETP(Instruction):

    def run(self, vm):
        vm.reg.PC += 1

        vm.stack[vm.reg.SP - 2] = getattr(vm.stack[vm.reg.SP - 2],
                                          str(vm.stack[vm.reg.SP - 1]))

        vm.reg.SP -= 1
