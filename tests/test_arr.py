#!/usr/bin/env python3
# coding: utf-8

from .base import BaseTest

class TestArr(BaseTest):

    def test_arr_0(self):
        '''
        a = [1, 2, 3]
        b = a[0]
        c = a[1]
        d = a[2]
        e = a['length']
        '''
        assert self.vm.frame.hash['b'] == 1
        assert self.vm.frame.hash['c'] == 2
        assert self.vm.frame.hash['d'] == 3
        assert self.vm.frame.hash['e'] == 3

    def test_arr_1(self):
        '''
        a = [1, 2, 3]
        a[1] = 10
        b = a[0]
        c = a[1]
        d = a[2]
        e = a.length
        '''
        assert self.vm.frame.hash['b'] == 1
        assert self.vm.frame.hash['c'] == 10
        assert self.vm.frame.hash['d'] == 3
        assert self.vm.frame.hash['e'] == 3
