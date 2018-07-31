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
        assert self.vm.stack[0] == 1.5
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
