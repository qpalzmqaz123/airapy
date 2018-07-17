#!/usr/bin/env python
# coding: utf-8

from pbl import Pbl

SCRIPT = '''\
a + 1
'''

if __name__ == '__main__':
    pbl = Pbl(10)

    tree = pbl.parse(SCRIPT)

    print(tree)
