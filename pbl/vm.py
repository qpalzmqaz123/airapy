#!/usr/bin/env python
# coding: utf-8

from enum import Enum, unique

@unique
class Register(Enum):
    PC = 1
    SP = 2

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Frame(object):

    def __init__(self, args=None):
        self.hash = {}

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self.__dict__))

    def __str__(self):
        return self.__repr__()

class VM(object):

    def __init__(self):
        self.reg = {}
        self.stack = [0] * 20
        self.frames = []
        self.frame = None

        for r in Register:
            self.reg[r] = 0

    def __repr__(self):
        return str(self.__dict__)

    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()
        self.frame = self.frames[-1] if self.frames else None
