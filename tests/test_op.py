#!/usr/bin/env python3
# coding: utf-8

from .base import BaseTest

class TestBinOp(BaseTest):

    def test_add(self):
        '''1 + 2'''
        assert self.vm.stack[0] == 3
        assert self.vm.reg.SP == 1

    def test_sub(self):
        '''2 - 1'''
        assert self.vm.stack[0] == 1
        assert self.vm.reg.SP == 1

    def test_mul(self):
        '''2 * 3'''
        assert self.vm.stack[0] == 6
        assert self.vm.reg.SP == 1

    def test_sub(self):
        '''3 / 2'''
        assert self.vm.stack[0] == 1
        assert self.vm.reg.SP == 1

    def test_sub_1(self):
        '''4 / 2'''
        assert self.vm.stack[0] == 2
        assert self.vm.reg.SP == 1

    def test_gt(self):
        '''
        1 > 2
        2 > 1
        '''
        assert self.vm.stack[0] == False
        assert self.vm.stack[1] == True
        assert self.vm.reg.SP == 2

    def test_lt(self):
        '''
        1 < 2
        2 < 1
        '''
        assert self.vm.stack[0] == True
        assert self.vm.stack[1] == False
        assert self.vm.reg.SP == 2

    def test_ge(self):
        '''
        1 >= 2
        2 >= 1
        2 >= 2
        '''
        assert self.vm.stack[0] == False
        assert self.vm.stack[1] == True
        assert self.vm.stack[2] == True
        assert self.vm.reg.SP == 3

    def test_le(self):
        '''
        1 <= 2
        2 <= 1
        2 <= 2
        '''
        assert self.vm.stack[0] == True
        assert self.vm.stack[1] == False
        assert self.vm.stack[2] == True
        assert self.vm.reg.SP == 3

    def test_eq(self):
        '''
        1 == 1
        1 == 2
        '''
        assert self.vm.stack[0] == True
        assert self.vm.stack[1] == False
        assert self.vm.reg.SP == 2

    def test_ne(self):
        '''
        1 != 1
        1 != 2
        '''
        assert self.vm.stack[0] == False
        assert self.vm.stack[1] == True
        assert self.vm.reg.SP == 2

class TestComplexOp(BaseTest):

    def test_1(self):
        '''1 + 2 + 3'''
        assert self.vm.stack[0] == 6

    def test_2(self):
        '''1 + 2 * 3'''
        assert self.vm.stack[0] == 7

    def test_3(self):
        '''(1 + 2) * 3'''
        assert self.vm.stack[0] == 9

class TestAssign(BaseTest):

    def test_eq(self):
        '''a = 1'''
        assert self.vm.frame.hash['a'] == 1

    def test_eq_expr(self):
        '''a = 1 + 1'''
        assert self.vm.frame.hash['a'] == 2

    def test_add_eq(self):
        '''
        a = 2
        a += 1
        '''
        assert self.vm.frame.hash['a'] == 3

    def test_sub_eq(self):
        '''
        a = 2
        a -= 1
        '''
        assert self.vm.frame.hash['a'] == 1

    def test_mul_eq(self):
        '''
        a = 2
        a *= 2
        '''
        assert self.vm.frame.hash['a'] == 4

    def test_div_eq(self):
        '''
        a = 2
        a /= 2
        '''
        assert self.vm.frame.hash['a'] == 1

    def test_get(self):
        '''
        a = 1
        b = 2
        c = a + b
        '''
        assert self.vm.frame.hash['a'] == 1
        assert self.vm.frame.hash['b'] == 2
        assert self.vm.frame.hash['c'] == 3
