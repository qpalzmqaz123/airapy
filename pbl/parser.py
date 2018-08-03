#!/usr/bin/env python
# coding: utf-8

import sys
import ply.yacc as yacc
from . import lexer
from . import ast

tokens = lexer.tokens

precedence = (
    ('right', 'EQUALS', 'ADDEQ', 'SUBEQ', 'MULEQ', 'DIVEQ'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'PERIOD', 'LSQUARE', 'RSQUARE'),
)

def p_program(p):
    '''program : stmt_list'''
    p[0] = p[1]

def p_stmt_list(p):
    '''stmt_list : stmt
                 | stmt_list stmt'''
    if (len(p) == 1):
        p[0] = ast.Block()
    elif (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        if not p[1]:
            p[1] = ast.Block()

        if not isinstance(p[1], ast.Block):
            p[1] = ast.Block().append(p[1])

        p[0] = p[1].append(p[2])

def p_stmt_newline(p):
    '''stmt : NEWLINE'''
    p[0] = ast.Block()

def p_stmt_expr(p):
    '''stmt : expr_stmt NEWLINE
            | while_stmt NEWLINE
            | if_stmt NEWLINE
            | return_stmt NEWLINE
            | break_stmt NEWLINE
            | continue_stmt NEWLINE'''
    p[0] = p[1]

def p_stmt_exprs(p):
    '''expr_stmt : assign_stmt
                 | test_stmt
                 | binop_stmt
                 | fn_stmt
                 | call_stmt
                 | array_stmt
                 | property_stmt'''
    p[0] = p[1]

def p_expr_stmt_identifer(p):
    '''expr_stmt : IDENTIFER'''
    p[0] = ast.Variable(p[1])

def p_expr_stmt_number(p):
    '''expr_stmt : NUMBER'''
    p[0] = ast.Int(int(p[1]))

def p_expr_stmt_float(p):
    '''expr_stmt : FLOAT'''
    p[0] = ast.Float(float(p[1]))

def p_expr_stmt_string(p):
    '''expr_stmt : STRING'''
    p[0] = ast.String(p[1])

def p_expr_stmt_nil(p):
    '''expr_stmt : NIL'''
    p[0] = ast.Nil()

def p_expr_stmt_true(p):
    '''expr_stmt : TRUE'''
    p[0] = ast.Boolean(True)

def p_expr_stmt_false(p):
    '''expr_stmt : FALSE'''
    p[0] = ast.Boolean(False)

def p_stmt_expr_assign(p):
    '''assign_stmt : IDENTIFER EQUALS expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), p[3])

def p_stmt_expr_assign_property(p):
    '''assign_stmt : property_stmt EQUALS expr_stmt'''
    p[0] = ast.Assign(p[1], p[3])

def p_stmt_expr_add_assign(p):
    '''assign_stmt : IDENTIFER ADDEQ expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), ast.BinOp(ast.Variable(p[1]), p[3], ast.BinOp.ADD))

def p_stmt_expr_sub_assign(p):
    '''assign_stmt : IDENTIFER SUBEQ expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), ast.BinOp(ast.Variable(p[1]), p[3], ast.BinOp.SUB))

def p_stmt_expr_mul_assign(p):
    '''assign_stmt : IDENTIFER MULEQ expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), ast.BinOp(ast.Variable(p[1]), p[3], ast.BinOp.MUL))

def p_stmt_expr_div_assign(p):
    '''assign_stmt : IDENTIFER DIVEQ expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), ast.BinOp(ast.Variable(p[1]), p[3], ast.BinOp.DIV))

def p_stmt_expr_assign_parent(p):
    '''assign_stmt : PARENT_IDENTIFER EQUALS expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), p[3], True)

def p_stmt_expr_add_assign_parent(p):
    '''assign_stmt : PARENT_IDENTIFER ADDEQ expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), ast.BinOp(ast.Variable(p[1]), p[3], ast.BinOp.ADD), True)

def p_stmt_expr_sub_assign_parent(p):
    '''assign_stmt : PARENT_IDENTIFER SUBEQ expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), ast.BinOp(ast.Variable(p[1]), p[3], ast.BinOp.SUB), True)

def p_stmt_expr_mul_assign_parent(p):
    '''assign_stmt : PARENT_IDENTIFER MULEQ expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), ast.BinOp(ast.Variable(p[1]), p[3], ast.BinOp.MUL), True)

def p_stmt_expr_div_assign_parent(p):
    '''assign_stmt : PARENT_IDENTIFER DIVEQ expr_stmt'''
    p[0] = ast.Assign(ast.Variable(p[1]), ast.BinOp(ast.Variable(p[1]), p[3], ast.BinOp.DIV), True)

def p_expr_stmt_gt(p):
    '''test_stmt : expr_stmt GT expr_stmt'''
    p[0] = ast.Compare(p[1], p[3], ast.Compare.GT)

def p_expr_stmt_ge(p):
    '''test_stmt : expr_stmt GE expr_stmt'''
    p[0] = ast.Compare(p[1], p[3], ast.Compare.GE)

def p_expr_stmt_lt(p):
    '''test_stmt : expr_stmt LT expr_stmt'''
    p[0] = ast.Compare(p[1], p[3], ast.Compare.LT)

def p_expr_stmt_le(p):
    '''test_stmt : expr_stmt LE expr_stmt'''
    p[0] = ast.Compare(p[1], p[3], ast.Compare.LE)

def p_expr_stmt_eq(p):
    '''test_stmt : expr_stmt EQ expr_stmt'''
    p[0] = ast.Compare(p[1], p[3], ast.Compare.EQ)

def p_expr_stmt_ne(p):
    '''test_stmt : expr_stmt NE expr_stmt'''
    p[0] = ast.Compare(p[1], p[3], ast.Compare.NE)

def p_expr_stmt_and(p):
    '''test_stmt : expr_stmt AND expr_stmt'''
    p[0] = ast.Test(p[1], p[3], ast.Test.AND)

def p_expr_stmt_or(p):
    '''test_stmt : expr_stmt OR expr_stmt'''
    p[0] = ast.Test(p[1], p[3], ast.Test.OR)

def p_expr_stmt_not(p):
    '''test_stmt : NOT expr_stmt'''
    p[0] = ast.Test(p[2], ast.Block(), ast.Test.NOT)

def p_expr_stmt_add(p):
    '''binop_stmt : expr_stmt PLUS expr_stmt'''
    p[0] = ast.BinOp(p[1], p[3], ast.BinOp.ADD)

def p_expr_stmt_sub(p):
    '''binop_stmt : expr_stmt MINUS expr_stmt'''
    p[0] = ast.BinOp(p[1], p[3], ast.BinOp.SUB)

def p_expr_stmt_mul(p):
    '''binop_stmt : expr_stmt TIMES expr_stmt'''
    p[0] = ast.BinOp(p[1], p[3], ast.BinOp.MUL)

def p_expr_stmt_div(p):
    '''binop_stmt : expr_stmt DIVIDE expr_stmt'''
    p[0] = ast.BinOp(p[1], p[3], ast.BinOp.DIV)

def p_expr_stmt_parenthesis(p):
    '''binop_stmt : LPAREN expr_stmt RPAREN'''
    p[0] = p[2]

def p_fn_stmt_multi_args(p):
    '''fn_stmt : FN LPAREN identifer_list IDENTIFER RPAREN DO stmt_list END'''
    p[0] = ast.Function(p[3].append(p[4]), p[7])

def p_fn_stmt_single_args(p):
    '''fn_stmt : FN LPAREN IDENTIFER RPAREN DO stmt_list END'''
    p[0] = ast.Function(ast.Arguments().append(p[3]), p[6])

def p_fn_stmt_empty_args(p):
    '''fn_stmt : FN LPAREN RPAREN DO stmt_list END'''
    p[0] = ast.Function(ast.Arguments(), p[5])

def p_fn_stmt_identifer_list(p):
    '''identifer_list : IDENTIFER COMMA
                      | identifer_list IDENTIFER COMMA'''
    if len(p) == 3:
        p[0] = ast.Arguments().append(p[1])
    elif len(p) == 4:
        p[0] = p[1].append(p[2])

def p_call_stmt_multi_args(p):
    '''call_stmt : callable_stmt LPAREN expr_stmt_list expr_stmt RPAREN'''
    p[0] = ast.Call(p[1], p[3].append(p[4]))

def p_call_stmt_single_args(p):
    '''call_stmt : callable_stmt LPAREN expr_stmt RPAREN'''
    p[0] = ast.Call(p[1], ast.Arguments().append(p[3]))

def p_call_stmt_empty_args(p):
    '''call_stmt : callable_stmt LPAREN RPAREN'''
    p[0] = ast.Call(p[1], ast.Arguments())

def p_array_stmt_empty_item(p):
    '''array_stmt : LSQUARE RSQUARE'''
    p[0] = ast.Array()

def p_array_stmt_single_item(p):
    '''array_stmt : LSQUARE expr_stmt RSQUARE'''
    p[0] = ast.Array().append(p[2])

def p_array_stmt_multi_item(p):
    '''array_stmt : LSQUARE array_expr_stmt_list expr_stmt RSQUARE'''
    p[0] = p[2].append(p[3])

def p_property_stmt(p):
    '''property_stmt : expr_stmt LSQUARE expr_stmt RSQUARE
                     | expr_stmt PERIOD IDENTIFER'''
    if len(p) == 5:
        p[0] = ast.Property(p[1], p[3])
    else:
        p[0] = ast.Property(p[1], ast.String(p[3]))

def p_stmt_while(p):
    '''while_stmt : WHILE expr_stmt DO stmt_list END'''
    p[0] = ast.While(p[2], p[4])

def p_expr_stmt_list(p):
    '''expr_stmt_list : expr_stmt COMMA
                      | expr_stmt_list expr_stmt COMMA'''
    if len(p) == 3:
        p[0] = ast.Arguments().append(p[1])
    elif len(p) == 4:
        p[0] = p[1].append(p[2])

def p_array_expr_stmt_list(p):
    '''array_expr_stmt_list : expr_stmt COMMA
                            | array_expr_stmt_list expr_stmt COMMA'''
    if len(p) == 3:
        p[0] = ast.Array().append(p[1])
    elif len(p) == 4:
        p[0] = p[1].append(p[2])

def p_if_stmt(p):
    '''if_stmt : IF expr_stmt DO stmt_list END'''
    p[0] = ast.If(p[2], p[4], ast.Block())

def p_if_else_stmt(p):
    '''if_stmt : IF expr_stmt DO stmt_list ELSE stmt_list END'''
    p[0] = ast.If(p[2], p[4], p[6])

# TODO elseif

def p_return_stmt(p):
    '''return_stmt : RETURN expr_stmt
                   | RETURN'''
    if len(p) == 3:
        p[0] = ast.Return(p[2])
    else:
        p[0] = ast.Return(None)

def p_break_stmt(p):
    '''break_stmt : BREAK'''
    p[0] = ast.Break()

def p_continue_stmt(p):
    '''continue_stmt : CONTINUE'''
    p[0] = ast.Continue()

def p_callable_stmt_identifer(p):
    '''callable_stmt : IDENTIFER'''
    p[0] = ast.Variable(p[1])

def p_callable_stmt_misc(p):
    '''callable_stmt : call_stmt
                     | property_stmt
                     | fn_stmt'''
    p[0] = p[1]

def p_error(p):
    if p:
        raise Exception("Syntax error at '%s' line %d" % (p.value, p.lineno))

parser = yacc.yacc()

def parse(script):
    if not (script.endswith('\r') or script.endswith('\n')):
        script += '\n'

    tree = parser.parse(script)

    return tree
