#!/usr/bin/env python
# coding: utf-8

from .compiler import Register

class VM(object):

    def __init__(self, stack_size=20):
        self.reg = {}
        self.stack = [0] * stack_size
        self.heap = []

        for r in Register:
            self.reg[r] = 0

    def __repr__(self):
        return str(self.__dict__)
