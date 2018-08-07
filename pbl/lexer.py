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
   'break': 'BREAK',
   'continue': 'CONTINUE',
   'nil': 'NIL',
   'and': 'AND',
   'or': 'OR',
   'not': 'NOT',
   'true': 'TRUE',
   'false': 'FALSE',
   'try': 'TRY',
   'catch': 'CATCH',
   'finally': 'FINALLY',
   'throw': 'THROW',
}

tokens = [
    'IDENTIFER', 'NUMBER', 'STRING', 'FLOAT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'ADDEQ', 'SUBEQ', 'MULEQ', 'DIVEQ',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
    'LPAREN','RPAREN', 'LSQUARE', 'RSQUARE', 'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'COLON',
    'NEWLINE',
] + list(reserved.values())

t_NUMBER  = r'[0-9]+'
t_FLOAT   = r'[0-9]+\.[0-9]+'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_ADDEQ   = r'\+='
t_SUBEQ   = r'\-='
t_MULEQ   = r'\*='
t_DIVEQ   = r'/='

t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='

t_COMMA  = r','
t_PERIOD = r'\.'
t_COLON  = r':'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'

def t_STRING(t):
    r"'(?:\\'|[^'])*?'"
    t.value = t.value[1:-1]
    t.value = t.value.replace("\\'", "'")
    return t

def t_IDENTIFER(t):
    r'@?[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFER')    # Check for reserved words
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_SPACE(t):
    r'\s+'
    pass

def t_error(t):
    raise Exception("Illegal character '%s' line %d" % (t.value[0], t.lineno))

lex.lex()
