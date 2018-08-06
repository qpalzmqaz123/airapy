#!/usr/bin/env python
# coding: utf-8

import time
from . import object as obj
from . import parser
from . import vm
from . import compiler

class Pbl(object):

    def __init__(self):
        self._vm = vm.VM()
        self.api = Api(self)

        self._vm.push_frame(vm.Frame())
        self._bootstrap()

    def parse(self, script):
        return parser.parse(script)

    def compile(self, tree):
        lst = compiler.InstructionList()

        tree.compile(lst)

        return lst

    def run(self, bytecode, debug=False):
        while True:
            if (self._vm.reg.PC >= len(bytecode)):
                break

            ins = bytecode[self._vm.reg.PC]
            ins.run(self._vm)

        if debug == False:
            self._vm.pop_frame()

        return self._vm

    def _bootstrap(self):
        self._setup_print()
        self._setup_error()

    def _setup_print(self):
        def _print(vm):
            nargs = vm.stack[vm.reg.SP - 2]
            args = vm.stack[vm.reg.SP - 2 - nargs : vm.reg.SP - 2]

            def _map(x):
                if x == None:
                    return 'nil'
                elif x == True:
                    return 'true'
                elif x == False:
                    return 'false'
                else:
                    return x

            print(*map(_map, args))

        global_obj = self.api.get_global_object()

        key = self.api.create_string('print')
        fn = self.api.create_function(_print)

        self.api.set_property(global_obj, key, fn)

    def _setup_error(self):
        def _error(vm):
            nargs = vm.stack[vm.reg.SP - 2]
            args = vm.stack[vm.reg.SP - 2 - nargs : vm.reg.SP - 2]

            message = '' if nargs == 0 else args[0]

            return obj.Error(message)

        global_obj = self.api.get_global_object()

        key = self.api.create_string('Error')
        fn = self.api.create_function(_error)

        self.api.set_property(global_obj, key, fn)

class Api(object):

    def __init__(self, pbl):
        self.pbl = pbl

    def get_global_object(self):
        return self.pbl._vm.frames[0].hash

    def set_property(self, target, key, value):
        target[key] = value

    def create_function(self, fn):
        return obj.BuiltinFunction(fn)

    def create_string(self, string):
        return string
