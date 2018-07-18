#!/usr/bin/env python
# coding: utf-8

from pbl import Pbl

SCRIPT = '''\
1 * (2 + 3 * (4 + 5 * (6 + 7)))
'''

if __name__ == '__main__':
    pbl = Pbl(10)

    tree = pbl.parse(SCRIPT)
    bytecode = pbl.compile(tree)

    print('\n------- script --------')
    print(SCRIPT)

    print('\n------- AST --------')
    print(tree)

    print('\n------- bytecode --------')
    print('\n'.join([str(x) for x in bytecode]))
