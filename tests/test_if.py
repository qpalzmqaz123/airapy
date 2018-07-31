#!/usr/bin/env python3
# coding: utf-8

from .base import BaseTest

class TestIf(BaseTest):

    def test_1(self):
        '''
        a = 1
        if 1 do
            a = 2
        end
        '''
        assert self.vm.frame.hash['a'] == 2

    def test_2(self):
        '''
        a = 1
        if 0 do
            a = 2
        else
            a = 3
        end
        '''
        assert self.vm.frame.hash['a'] == 3
