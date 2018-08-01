#!/usr/bin/env python
# coding: utf-8

class Object(object):
    pass

class Function(Object):

    def __init__(self, index, parent_frame):
        self.index = index
        self.parent_frame = parent_frame
