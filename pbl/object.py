#!/usr/bin/env python
# coding: utf-8

class Object(object):
    pass

class Function(Object):

    def __init__(self, index, parent_frame):
        self.index = index
        self.parent_frame = parent_frame

class Array(Object):

    def __init__(self):
        self.list = []

    def append(self, value):
        self.list.append(value)

    @property
    def length(self):
        return len(self.list)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str(self.list))
