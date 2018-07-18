#!/usr/bin/env python
# coding: utf-8

from . import compiler
from .compiler import Register

class Tree(object):

    def eval(self):
        pass

    def compile(self):
        pass

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self.__dict__))

    def __str__(self):
        return self.__repr__()

class Node(Tree):
    pass

class Block(Tree):

    def __init__(self):
        self.list = []

    def append(self, node):
        if (node):
            self.list.append(node)

        return self

    def __iter__(self):
        return iter(self.list)

class Int(Node):

    def __init__(self, n):
        self.value = n

    def compile(self):
        return [compiler.LOADC(int(self.value), Register.R0)]

class Float(Node):

    def __init__(self, f):
        self.value = f

class String(Node):

    def __init__(self, s):
        self.value = s

class Variable(Node):

    def __init__(self, name):
        self.name = name

class BinOp(Node):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'

    def __init__(self, left, right, type):
        self.left = left
        self.right = right
        self.type = type

    def compile(self):
        i_arr = []

        i_arr += self.left.compile()
        i_arr.append(compiler.PUSH(Register.R0))

        i_arr += self.right.compile()
        i_arr.append(compiler.POP(Register.R1))

        if self.type == self.ADD:
            i_arr.append(compiler.ADD(Register.R1, Register.R0))
        elif self.type == self.SUB:
            i_arr.append(compiler.SUB(Register.R1, Register.R0))
        elif self.type == self.MUL:
            i_arr.append(compiler.MUL(Register.R1, Register.R0))
        elif self.type == self.DIV:
            i_arr.append(compiler.DIV(Register.R1, Register.R0))
        else:
            raise Exception('Invliad operation: %s' % self.type)

        return i_arr

class Assign(Node):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

class Compare(Node):
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='

    def __init__(self, left, right, type):
        self.left = left
        self.right = right
        self.type = type

class While(Node):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class If(Node):

    def __init__(self, condition, body, otherwise):
        self.condition = condition
        self.body = body
        self.otherwise = otherwise

class Function(Node):

    def __init__(self, args, body):
        self.args = args
        self.body = body

class Arguments(Node):

    def __init__(self):
        self.list = []

    def append(self, node):
        self.list.append(node)

        return self

    def __repr__(self):
        values = ['list=%s' % self.list]

        return type(self).__name__ + '(' + ', '.join(values) + ')'

class Return(Node):

    def __init__(self, expr):
        self.expr = expr

class Call(Node):

    def __init__(self, fn, args):
        self.fn = fn
        self.args = args
