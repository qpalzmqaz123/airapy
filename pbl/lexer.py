#!/usr/bin/env python
# coding: utf-8

import sys
import ply.lex as lex

reserved = {
   'while': 'WHILE',
   'do': 'DO',
   'end': 'END',
   'fn': 'FN',
   'return': 'RETURN',
   'if': 'IF',
   'else': 'ELSE',
}

tokens = [
    'IDENTIFER', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'GT', 'LT', 'GE', 'LE',
    'LPAREN','RPAREN',
    'COMMA',
    'NEWLINE',
] + list(reserved.values())

t_NUMBER  = r'[0-9]+'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='

t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='

t_COMMA = r','

t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_IDENTIFER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFER')    # Check for reserved words
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_SPACE(t):
    r'\s+'
    pass

def t_error(t):
    raise Exception("Illegal character '%s' line %d" % (t.value[0], t.lineno))

lex.lex()
