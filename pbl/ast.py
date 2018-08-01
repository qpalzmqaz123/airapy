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
    NE = '!='

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
        elif self.type == self.NE:
            lst.append(compiler.NE())
        else:
            raise Exception('Invliad operation: %s' % self.type)

class While(Node):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def compile(self, lst):
        #   PUSHL (push loop)
        # a ... (condition)
        # b JMPF c
        #   ...
        #   POPL (break)
        #   ...
        #   CONT (continue)
        #   ...
        #   CONT
        # c POPL
        #   ...
        index_a = lst.lastIndex + 2
        lst.append(compiler.PUSHL(-1))

        self.condition.compile(lst)

        index_b = lst.lastIndex + 1
        lst.append(compiler.JMPF(-1))

        self.body.compile(lst)

        lst.append(compiler.CONT())

        index_c = lst.lastIndex + 1
        lst.append(compiler.POPL())

        lst[index_a - 1].index = index_c
        lst[index_b].index = index_c

class If(Node):

    def __init__(self, condition, body, otherwise):
        self.condition = condition
        self.body = body
        self.otherwise = otherwise

    def compile(self, lst):
        #   ... (condition)
        # a JMPT b
        #   ... (false)
        #   JMP c
        # b ... (true)
        # c ...
        self.condition.compile(lst)

        index_a = lst.lastIndex + 1
        lst.append(compiler.JMPT(-1))

        self.otherwise.compile(lst)

        lst.append(compiler.JMP(-1))

        index_b = lst.lastIndex + 1

        self.body.compile(lst)

        index_c = lst.lastIndex + 1

        lst[index_a].index = index_b
        lst[index_b - 1].index = index_c

class Function(Node):

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def compile(self, lst):
        #   ...
        # a JMP b
        #   ... (function body)
        # b ...
        index = -1 - len(self.args)

        lst.append(compiler.JMP(-1))
        index_a = lst.lastIndex

        if (len(self.args)):
            for k in self.args:
                lst.append(compiler.DUP(index))
                lst.append(compiler.SET(k))
                lst.append(compiler.POP())

                index += 1

        self.body.compile(lst)
        lst.append(compiler.RET())
        index_b = lst.lastIndex + 1

        lst.append(compiler.MKFN(index_a + 1))

        lst[index_a].index = index_b

class Arguments(Node):

    def __init__(self):
        self.list = []

    def append(self, node):
        self.list.append(node)

        return self

    def __repr__(self):
        values = ['list=%s' % self.list]

        return type(self).__name__ + '(' + ', '.join(values) + ')'

    def __iter__(self):
        return iter(self.list)

    def __len__(self):
        return len(self.list)

    def compile(self, lst):
        for node in self:
            node.compile(lst)

class Return(Node):

    def __init__(self, expr):
        self.expr = expr

    def compile(self, lst):
        if not self.expr:
            lst.append(compiler.PUSH(None))
        else:
            self.expr.compile(lst)

        lst.append(compiler.RET())

class Call(Node):

    def __init__(self, fn, args):
        self.fn = fn
        self.args = args

    def compile(self, lst):
        # ...
        # SP
        # ... (args)
        # ... (function body)
        lst.append(compiler.PUSHR('SP'))

        self.args.compile(lst)
        self.fn.compile(lst)

        lst.append(compiler.CALL())

class Break(Node):

    def compile(self, lst):
        lst.append(compiler.POPL())

class Continue(Node):

    def compile(self, lst):
        lst.append(compiler.CONT())
