#!/usr/bin/env python
# coding: utf-8

from pbl import Pbl

SCRIPT = '''\
a = 1
b = 2
c = 0
if a == 1 do
    if b == 2 do
        c = 3
    else
        c = 5
    end
else
    c = 4
end
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
    print('\n'.join(['%4d %s' % (i, str(bytecode[i])) for i in range(len(bytecode))]))

    print('\n------- run --------')
    pbl.run(bytecode)
