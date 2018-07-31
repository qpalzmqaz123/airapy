#!/usr/bin/env python3
# coding: utf-8

from .base import BaseTest

class TestWhile(BaseTest):

    def test_1(self):
        '''
        a = 0
        sum = 0

        while a < 5 do
            a += 1
            sum += 1
        end
        '''
        assert self.vm.frame.hash['sum'] == 5
