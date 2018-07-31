#!/usr/bin/env python3
# coding: utf-8

from pbl import Pbl

def case(fn):
    def wrapper(self):
        script = fn.__doc__
        if not script:
            raise TypeError('script is not defined')

        pbl = Pbl()
        tree = pbl.parse(script)
        bytecode = pbl.compile(tree)
        self.vm = pbl.run(bytecode, debug=True)

        fn(self)

    return wrapper

class MetaTest(type):

    def __new__(cls, clsname, bases, dct):
        if clsname != 'BaseTest':
            for (key, value) in dct.items():
                if key.startswith('test'):
                    dct[key] = case(value)

        return type.__new__(cls, clsname, bases, dct)

class BaseTest(object, metaclass=MetaTest):
    pass
