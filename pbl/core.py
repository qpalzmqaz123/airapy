#!/usr/bin/env python
# coding: utf-8

import time
from . import parser
from . import vm
from . import compiler

class Pbl(object):

    def __init__(self, memblk=1000):
        self._vm = vm.VM()

    def parse(self, script):
        return parser.parse(script)

    def compile(self, tree):
        lst = compiler.InstructionList()

        tree.compile(lst)

        return lst

    def run(self, bytecode, debug=False):
        frame = vm.Frame()

        self._vm.push_frame(frame)

        while True:
            if (self._vm.reg.PC >= len(bytecode)):
                break

            ins = bytecode[self._vm.reg.PC]
            ins.run(self._vm)

        if debug == False:
            self._vm.pop_frame()

        return self._vm
