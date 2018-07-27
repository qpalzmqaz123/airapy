#!/usr/bin/env python
# coding: utf-8

from pbl import Pbl

SCRIPT = '''\
fn1 = fn(v) do
    v += 2

    return v
end

a = fn1(1)
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
    frame = pbl.run(bytecode, debug=True)

    print(frame)
