#!/usr/bin/env python
# coding: utf-8

from . import parser
from . import vm
from .compiler import Register

class Pbl(object):

    def __init__(self, memblk=1000):
        self._vm = vm.VM()

    def parse(self, script):
        return parser.parse(script)

    def compile(self, tree):
        return tree.compile()

    def run(self, bytecode):
        while True:
            if (self._vm.reg[Register.PC] >= len(bytecode)):
                break

            ins = bytecode[self._vm.reg[Register.PC]]
            ins.run(self._vm)

        print(self._vm)
