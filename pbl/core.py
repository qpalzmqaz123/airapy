#!/usr/bin/env python
# coding: utf-8

from . import parser

class Pbl(object):

    def __init__(self, memblk=1000):
        pass

    def parse(self, script):
        tree = parser.parse(script)
        print(tree)

    def run(self, bytecode):
        pass
