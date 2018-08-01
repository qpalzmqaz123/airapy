#!/usr/bin/env python
# coding: utf-8

import os
import sys
import click
from pbl import Pbl

@click.command()
@click.option('--debug', default=False, help='Show debug info.', is_flag=True)
@click.argument('file')
def main(debug, file):
    script = get_script(file)
    if debug:
        print('\n------- script  -------')
        print(script)

    pbl = Pbl()

    tree = pbl.parse(script)
    if debug:
        print('\n------- AST -------')
        print(tree)

    bytecode = pbl.compile(tree)
    if debug:
        print('\n------- bytecode -------')
        print('\n'.join(['%4d %s' % (i, str(bytecode[i])) for i in range(len(bytecode))]))

    frame = pbl.run(bytecode, debug=True)

    if debug:
        print('\n------- frame -------')
        print(frame)

def get_script(path):
    current_path = os.getcwd()
    file_path = os.path.join(current_path, path)

    script = ''
    with open(file_path) as f:
        script = f.read()

    return script

if __name__ == '__main__':
    main()
