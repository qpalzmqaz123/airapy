#!/usr/bin/env python
# coding: utf-8

class Register(object):
    def __init__(self):
        self.PC = 0
        self.SP = 0

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self.__dict__))

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        return getattr(self, key)

class Frame(object):

    def __init__(self):
        self.hash = {}
        self.loop = []
        self.reg = Register()

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self.__dict__))

    def __str__(self):
        return self.__repr__()

class VM(object):

    def __init__(self):
        self.reg = None
        self.stack = [0] * 20
        self.frames = []
        self.frame = None

    def __repr__(self):
        return str(self.__dict__)

    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

        if self.reg:
            self.frame.reg.PC = self.reg.PC
            self.frame.reg.SP = self.reg.SP

        self.reg = self.frame.reg

    def pop_frame(self):
        self.frames.pop()
        self.frame = self.frames[-1] if self.frames else None
        self.reg = self.frames[-1].reg if self.frames else None
