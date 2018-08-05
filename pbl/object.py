#!/usr/bin/env python
# coding: utf-8

import re

class Object(object):
    pass

class Function(Object):

    def __init__(self, index, parent_frame):
        self.index = index
        self.parent_frame = parent_frame

class BuiltinFunction(Object):

    def __init__(self, fn):
        self.fn = fn

class Array(Object):

    def __init__(self):
        self.list = []

    def append(self, value):
        self.list.append(value)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self.list))

    def __getattr__(self, attr):
        if re.match(r'^\d+$', attr):
            return self.list[int(attr)]
        elif attr == 'length':
            return len(self.list)
        else:
            return super().__getattr__(attr)

    def __setattr__(self, attr, value):
        if re.match(r'^\d+$', attr):
            self.list[int(attr)] = value
        else:
            super().__setattr__(attr, value)

    @property
    def length(self):
        return len(self.list)

    @property
    def push(self):
        def _fn(vm):
            assert vm.stack[vm.reg.SP - 2] == 1

            value = vm.stack[vm.reg.SP - 3]
            self.list.append(value)

            return value

        return BuiltinFunction(_fn)

    @property
    def pop(self):
        def _fn(vm):
            # remove last element
            if vm.stack[vm.reg.SP - 2] == 0:
                value = self.list.pop()
            elif vm.stack[vm.reg.SP - 2] == 1:
                value = self.list.pop(vm.stack[vm.reg.SP - 3])
            else:
                raise Exception('Invliad args count')

            return value

        return BuiltinFunction(_fn)

    @property
    def insert(self):
        def _fn(vm):
            assert vm.stack[vm.reg.SP - 2] == 2

            index = vm.stack[vm.reg.SP - 4]
            value = vm.stack[vm.reg.SP - 3]

            self.list.insert(index, value)

            return value

        return BuiltinFunction(_fn)

class Hash(Object):

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self.__dict__))

    def __getattr__(self, attr):
        return super().__getattr__(attr)

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
