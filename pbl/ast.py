#!/usr/bin/env python
# coding: utf-8

from . import compiler

class Tree(object):

    def __init__(self, line=0, text=''):
        self.line = line
        self.text = text

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

    def __init__(self, n, line, text):
        super().__init__(line=line, text=text)

        self.value = n

    def compile(self, lst):
        lst.append(compiler.PUSH(int(self.value), line=self.line, text=self.text))

class Float(Node):

    def __init__(self, f, line, text):
        super().__init__(line=line, text=text)

        self.value = f

    def compile(self, lst):
        lst.append(compiler.PUSH(float(self.value), line=self.line, text=self.text))

class String(Node):

    def __init__(self, s, line, text):
        super().__init__(line=line, text=text)

        self.value = s

    def compile(self, lst):
        lst.append(compiler.PUSH(self.value, line=self.line, text=self.text))

class Nil(Node):

    def __init__(self, line, text):
        super().__init__(line=line, text=text)

    def compile(self, lst):
        lst.append(compiler.PUSH(None, line=self.line, text=self.text))

class Variable(Node):

    def __init__(self, name, line=0, text=''):
        super().__init__(line, text)

        self.name = name

    def compile(self, lst, is_get=True):
        lst.append(compiler.GET(self.name, line=self.line, text=self.text) if is_get else compiler.SET(self.name, line=self.line, text=self.text))

class Property(Node):

    def __init__(self, target, key, line=0, text=''):
        super().__init__(line, text)

        self.target = target
        self.key = key

    def compile(self, lst, is_get=True):
            self.target.compile(lst)
            self.key.compile(lst)
            lst.append(compiler.GETP(line=self.line, text=self.text) if is_get else compiler.SETP(line=self.line, text=self.text))

class Boolean(Node):

    def __init__(self, value, line, text):
        super().__init__(line=line, text=text)

        self.value = bool(value)

    def compile(self, lst):
        lst.append(compiler.PUSH(self.value, line=self.line, text=self.text))

class Array(Node):

    def __init__(self, line, text):
        super().__init__(line=line, text=text)

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

        lst.append(compiler.MKARR(len(self.list), line=self.line, text=self.text))

class Hash(Node):

    def __init__(self, line, text):
        super().__init__(line=line, text=text)

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

        lst.append(compiler.MKHASH(len(items), line=self.line, text=self.text))

class BinOp(Node):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'

    def __init__(self, left, right, type, line, text):
        super().__init__(line=line, text=text)

        self.left = left
        self.right = right
        self.type = type

    def compile(self, lst):
        self.left.compile(lst)
        self.right.compile(lst)

        if self.type == self.ADD:
            lst.append(compiler.ADD(line=self.line, text=self.text))
        elif self.type == self.SUB:
            lst.append(compiler.SUB(line=self.line, text=self.text))
        elif self.type == self.MUL:
            lst.append(compiler.MUL(line=self.line, text=self.text))
        elif self.type == self.DIV:
            lst.append(compiler.DIV(line=self.line, text=self.text))
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

    def __init__(self, left, right, type, line, text):
        super().__init__(line=line, text=text)

        self.left = left
        self.right = right
        self.type = type

    def compile(self, lst):
        self.left.compile(lst)
        self.right.compile(lst)

        if self.type == self.GT:
            lst.append(compiler.GT(line=self.line, text=self.text))
        elif self.type == self.GE:
            lst.append(compiler.GE(line=self.line, text=self.text))
        elif self.type == self.LT:
            lst.append(compiler.LT(line=self.line, text=self.text))
        elif self.type == self.LE:
            lst.append(compiler.LE(line=self.line, text=self.text))
        elif self.type == self.EQ:
            lst.append(compiler.EQ(line=self.line, text=self.text))
        elif self.type == self.NE:
            lst.append(compiler.NE(line=self.line, text=self.text))
        else:
            raise Exception('Invliad operation: %s' % self.type)

class Test(Node):
    AND = 'and'
    OR = 'or'
    NOT = 'not'

    def __init__(self, left, right, type, line, text):
        super().__init__(line=line, text=text)

        self.left = left
        self.right = right
        self.type = type

    def compile(self, lst):
        self.left.compile(lst)
        self.right.compile(lst)

        if self.type == self.AND:
            lst.append(compiler.AND(line=self.line, text=self.text))
        elif self.type == self.OR:
            lst.append(compiler.OR(line=self.line, text=self.text))
        elif self.type == self.NOT:
            lst.append(compiler.NOT(line=self.line, text=self.text))
        else:
            raise Exception('Invliad type: %s' % self.type)

class While(Node):

    def __init__(self, condition, body, line, text):
        super().__init__(line=line, text=text)

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
        lst.append(compiler.PUSHL(-1, line=self.line, text=self.text))

        self.condition.compile(lst)

        index_b = lst.lastIndex + 1
        lst.append(compiler.JMPF(-1, line=self.line, text=self.text))

        self.body.compile(lst)

        lst.append(compiler.CONT(line=self.line, text=self.text))

        index_c = lst.lastIndex + 1
        lst.append(compiler.POPL(line=self.line, text=self.text))

        lst[index_a - 1].index = index_c
        lst[index_b].index = index_c

class If(Node):

    def __init__(self, condition, body, otherwise, line, text):
        super().__init__(line=line, text=text)

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
        lst.append(compiler.JMPT(-1, line=self.line, text=self.text))

        self.otherwise.compile(lst)

        lst.append(compiler.JMP(-1))

        index_b = lst.lastIndex + 1

        self.body.compile(lst)

        index_c = lst.lastIndex + 1

        lst[index_a].index = index_b
        lst[index_b - 1].index = index_c

class Function(Node):

    def __init__(self, args, body, line, text):
        super().__init__(line, text)

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
                lst.append(compiler.DUP(index, line=self.line, text=self.text))
                lst.append(compiler.SET(k, line=self.line, text=self.text))
                lst.append(compiler.POP(line=self.line, text=self.text))

                index += 1

        self.body.compile(lst)
        lst.append(compiler.PUSH(None, line=self.line, text=self.text))
        lst.append(compiler.RET(line=self.line, text=self.text))
        index_b = lst.lastIndex + 1

        lst.append(compiler.MKFN(index_a + 1, line=self.line, text=self.text))

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

    def __init__(self, expr, line, text):
        super().__init__(line=line, text=text)

        self.expr = expr

    def compile(self, lst):
        if not self.expr:
            lst.append(compiler.PUSH(None, line=self.line, text=self.text))
        else:
            self.expr.compile(lst)

        lst.append(compiler.RET(line=self.line, text=self.text))

class Call(Node):

    def __init__(self, fn, args, line=0):
        super().__init__(line)

        self.fn = fn
        self.args = args

    def compile(self, lst):
        # ...
        # ... (args)
        # ... (nargs)
        # ... (function body)
        # ...
        self.args.compile(lst)
        lst.append(compiler.PUSH(len(self.args), line=self.line, text=self.text))
        self.fn.compile(lst)

        lst.append(compiler.CALL(line=self.line, text=self.fn.text))

class Break(Node):

    def __init__(self, line, text):
        super().__init__(line=line, text=text)

    def compile(self, lst):
        lst.append(compiler.POPL(line=self.line, text=self.text))

class Continue(Node):

    def __init__(self, line, text):
        super().__init__(line=line, text=text)

    def compile(self, lst):
        lst.append(compiler.CONT(line=self.line, text=self.text))
