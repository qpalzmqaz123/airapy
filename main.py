#!/usr/bin/env python
# coding: utf-8

from pbl import Pbl

SCRIPT = '''\
a + 1
'''

if __name__ == '__main__':
    pbl = Pbl(10)

    bytecode = pbl.parse(SCRIPT)

    print(bytecode)

    result = pbl.run(bytecode)

