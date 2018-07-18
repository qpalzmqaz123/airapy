#!/usr/bin/env python
# coding: utf-8

from pbl import Pbl

SCRIPT = '''\
1 * (2 + 3 * (4 + 5 * (6 + 7)))
'''

if __name__ == '__main__':
    pbl = Pbl(10)

    tree = pbl.parse(SCRIPT)

    print('------- script --------')
    print(SCRIPT)

    print('------- AST --------')
    print(tree)

    print('------- bytecode --------')
    i_arr = tree.compile()
    for i in i_arr:
        print(i)
