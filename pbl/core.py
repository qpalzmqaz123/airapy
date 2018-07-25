#!/usr/bin/env python
# coding: utf-8

from . import parser
from . import vm

class Pbl(object):

    def __init__(self, memblk=1000):
        self._vm = vm.VM()

    def parse(self, script):
        return parser.parse(script)

    def compile(self, tree):
        return tree.compile()

    def run(self, bytecode):
        frame = vm.Frame()

        self._vm.push_frame(frame)

        while True:
            if (self._vm.reg.PC >= len(bytecode)):
                break

            ins = bytecode[self._vm.reg.PC]
            ins.run(self._vm)

#        self._vm.pop_frame()

        print(self._vm)
