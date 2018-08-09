#!/usr/bin/env python
# coding: utf-8

import time
from . import object as obj
from . import parser
from . import vm
from . import compiler

class Aira(object):

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
            if len(self._vm.frames) == 1 and self._vm.frame.error:
                self.error_handler(self._vm.frame.error)
                return self._vm

            if (self._vm.reg.PC >= len(bytecode)):
                break

            ins = bytecode[self._vm.reg.PC]
            ins.run(self._vm)

        if debug == False:
            self._vm.pop_frame()

        return self._vm

    def error_handler(self, err):
        print(err)

    def _bootstrap(self):
        self._setup_print()
        self._setup_error()

    def _setup_print(self):
        # print(...)
        def _print(vm):
            nargs = vm.stack[vm.reg.SP - 2]
            args = vm.stack[vm.reg.SP - 2 - nargs : vm.reg.SP - 2]

            def _map(x):
                if x == None:
                    return 'nil'
                elif x == True and isinstance(x, bool):
                    return 'true'
                elif x == False and isinstance(x, bool):
                    return 'false'
                else:
                    return x

            print(*map(_map, args))

        global_obj = self.api.get_global_object()

        key = self.api.create_string('print')
        fn = self.api.create_function(_print)

        self.api.set_property(global_obj, key, fn)

    def _setup_error(self):
        # Error(msg)
        def _error(vm):
            nargs = vm.stack[vm.reg.SP - 2]
            args = vm.stack[vm.reg.SP - 2 - nargs : vm.reg.SP - 2]

            message = '' if nargs == 0 else args[0]

            backtrace = []

            for frame in vm.frames[1:]:
                backtrace.append({
                    'line': frame.line,
                    'text': frame.text
                })

            return obj.Error(message, backtrace)

        global_obj = self.api.get_global_object()

        key = self.api.create_string('Error')
        fn = self.api.create_function(_error)

        self.api.set_property(global_obj, key, fn)

class Api(object):

    def __init__(self, aira):
        self.aira = aira

    def get_global_object(self):
        return self.aira._vm.frames[0].hash

    def set_property(self, target, key, value):
        target[key] = value

    def create_function(self, fn):
        return obj.BuiltinFunction(fn)

    def create_string(self, string):
        return string

    def create_int(self, num):
        return num
