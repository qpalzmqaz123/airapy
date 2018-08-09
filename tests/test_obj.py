#!/usr/bin/env python3
# coding: utf-8

from .base import BaseTest

class TestObj(BaseTest):

    def test_int(self):
        '''1'''
        assert self.vm.stack[0] == 1

    def test_string(self):
        '''
        'abc'
        '''
        assert self.vm.stack[0] == 'abc'

    def test_string_escape(self):
        '''
        'ab\\'c'
        '''
        assert self.vm.stack[0] == 'ab\'c'

    def test_string_escape_1(self):
        '''
        'ab"c'
        '''
        assert self.vm.stack[0] == 'ab"c'

    def test_string_escape_dq(self):
        '''
        "ab'c"
        '''
        assert self.vm.stack[0] == 'ab\'c'

    def test_string_escape_dq_1(self):
        '''
        "ab\\"c"
        '''
        assert self.vm.stack[0] == 'ab"c'

    def test_nil(self):
        '''nil'''
        assert self.vm.stack[0] == None

    def test_float(self):
        '''1.1'''
        assert self.vm.stack[0] == 1.1

    def test_true(self):
        '''true'''
        assert self.vm.stack[0] == True

    def test_false(self):
        '''false'''
        assert self.vm.stack[0] == False
