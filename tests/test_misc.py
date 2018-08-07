#!/usr/bin/env python3
# coding: utf-8

from .base import BaseTest

class TestMisc(BaseTest):

    def test_fibonacci(self):
        '''
        n = 10

        res = []

        sum = fn(index) do
            if index <= 0 do
                throw Error('index must be greater than 0')
            end

            if index == 1 or index == 2 do
                return 1
            end

            return sum(index - 1) + sum(index - 2)
        end

        i = 1
        while i < n + 1do
            res.push(sum(i))

            i += 1
        end
        '''
        assert self.vm.frame.hash['res'].list == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
