#!/usr/bin/env python
# coding: utf-8

from . import compiler

class Tree(object):

    def eval(self):
        pass

    def compile(self, lst):
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

    def compile(self, lst):
        for tree in self:
            try:
                tree.compile(lst)
            except TypeError as err:
                print('Compile error:', str(tree))

                raise err

class Int(Node):

    def __init__(self, n):
        self.value = n

    def compile(self, lst):
        lst.append(compiler.PUSH(int(self.value)))

class Float(Node):

    def __init__(self, f):
        self.value = f

class String(Node):

    def __init__(self, s):
        self.value = s

class Variable(Node):

    def __init__(self, name):
        self.name = name

    def compile(self, lst):
        lst.append(compiler.GET(self.name))

class BinOp(Node):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'

    def __init__(self, left, right, type):
        self.left = left
        self.right = right
        self.type = type

    def compile(self, lst):
        self.left.compile(lst)
        self.right.compile(lst)

        if self.type == self.ADD:
            lst.append(compiler.ADD())
        elif self.type == self.SUB:
            lst.append(compiler.SUB())
        elif self.type == self.MUL:
            lst.append(compiler.MUL())
        elif self.type == self.DIV:
            lst.append(compiler.DIV())
        else:
            raise Exception('Invliad operation: %s' % self.type)

class Assign(Node):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def compile(self, lst):
        self.value.compile(lst)
        lst.append(compiler.SET(self.variable.name))

class Compare(Node):
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='
    EQ = '=='

    def __init__(self, left, right, type):
        self.left = left
        self.right = right
        self.type = type

    def compile(self, lst):
        self.left.compile(lst)
        self.right.compile(lst)

        if self.type == self.GT:
            lst.append(compiler.GT())
        elif self.type == self.GE:
            lst.append(compiler.GE())
        elif self.type == self.LT:
            lst.append(compiler.LT())
        elif self.type == self.LE:
            lst.append(compiler.LE())
        elif self.type == self.EQ:
            lst.append(compiler.EQ())
        else:
            raise Exception('Invliad operation: %s' % self.type)

class While(Node):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class If(Node):

    def __init__(self, condition, body, otherwise):
        self.condition = condition
        self.body = body
        self.otherwise = otherwise

    def compile(self, lst):
        self.condition.compile(lst)

        index_else = lst.lastIndex + 1

        self.otherwise.compile(lst)

        index_if = lst.lastIndex + 1

        self.body.compile(lst)

        index_out = lst.lastIndex + 1

        lst.insert(index_else, compiler.JMPT(index_if + 2))
        lst.insert(index_if + 1, compiler.JMP(index_out + 2))

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
