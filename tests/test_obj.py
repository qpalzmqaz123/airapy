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

    def test_nil(self):
        '''nil'''
        assert self.vm.stack[0] == None