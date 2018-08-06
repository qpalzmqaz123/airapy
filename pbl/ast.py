#!/usr/bin/env python
# coding: utf-8

from . import compiler

class Tree(object):

    def __init__(self, line=0, col=0):
        self.line = line
        self.col = col

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

    def compile(self, lst):
        lst.append(compiler.PUSH(float(self.value)))

class String(Node):

    def __init__(self, s):
        self.value = s

    def compile(self, lst):
        lst.append(compiler.PUSH(self.value))

class Nil(Node):

    def compile(self, lst):
        lst.append(compiler.PUSH(None))

class Variable(Node):

    def __init__(self, name):
        self.name = name

    def compile(self, lst, is_get=True):
        lst.append(compiler.GET(self.name) if is_get else compiler.SET(self.name))

class Property(Node):

    def __init__(self, target, key):
        self.target = target
        self.key = key

    def compile(self, lst, is_get=True):
            self.target.compile(lst)
            self.key.compile(lst)
            lst.append(compiler.GETP() if is_get else compiler.SETP())

class Boolean(Node):

    def __init__(self, value):
        self.value = bool(value)

    def compile(self, lst):
        lst.append(compiler.PUSH(self.value))

class Array(Node):

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

        lst.append(compiler.MKARR(len(self.list)))

class Hash(Node):

    def __init__(self):
        self.hash = {}

    def __repr__(self):
        values = ['hash=%s' % self.hash]

        return type(self).__name__ + '(' + ', '.join(values) + ')'

    def set(self, key_value):
        self.hash[key_value[0]] = key_value[1]

        return self

    def compile(self, lst):

        items = self.hash.items()

        for key, value in items:
            key.compile(lst)
            value.compile(lst)

        lst.append(compiler.MKHASH(len(items)))

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

        self.variable.compile(lst, False)

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

class Test(Node):
    AND = 'and'
    OR = 'or'
    NOT = 'not'

    def __init__(self, left, right, type):
        self.left = left
        self.right = right
        self.type = type

    def compile(self, lst):
        self.left.compile(lst)
        self.right.compile(lst)

        if self.type == self.AND:
            lst.append(compiler.AND())
        elif self.type == self.OR:
            lst.append(compiler.OR())
        elif self.type == self.NOT:
            lst.append(compiler.NOT())
        else:
            raise Exception('Invliad type: %s' % self.type)

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
        index = -2 - len(self.args)

        lst.append(compiler.JMP(-1))
        index_a = lst.lastIndex

        if (len(self.args)):
            for k in self.args:
                lst.append(compiler.DUP(index))
                lst.append(compiler.SET(k))
                lst.append(compiler.POP())

                index += 1

        self.body.compile(lst)
        lst.append(compiler.PUSH(None))
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
        # ... (args)
        # ... (nargs)
        # ... (function body)
        # ...
        self.args.compile(lst)
        lst.append(compiler.PUSH(len(self.args)))
        self.fn.compile(lst)

        lst.append(compiler.CALL())

class Break(Node):

    def compile(self, lst):
        lst.append(compiler.POPL())

class Continue(Node):

    def compile(self, lst):
        lst.append(compiler.CONT())
