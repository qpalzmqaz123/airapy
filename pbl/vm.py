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

class Frame(object):

    def __init__(self, args=None):
        self.hash = {}

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self.__dict__))

    def __str__(self):
        return self.__repr__()

class VM(object):

    def __init__(self):
        self.reg = Register()
        self.stack = [0] * 20
        self.frames = []
        self.frame = None

    def __repr__(self):
        return str(self.__dict__)

    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()
        self.frame = self.frames[-1] if self.frames else None
