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

    def test_arr_push(self):
        '''
        a = [1, 2, 3]
        a.push(100)
        '''
        assert self.vm.frame.hash['a'].list == [1, 2, 3, 100]

    def test_arr_pop(self):
        '''
        a = [1, 2, 3, 4, 5]
        a.pop()
        a.pop(1)
        '''
        assert self.vm.frame.hash['a'].list == [1, 3, 4]

    def test_arr_insert(self):
        '''
        a = [1, 2, 3]
        a.insert(1, 100)
        '''
        assert self.vm.frame.hash['a'].list == [1, 100, 2, 3]

    def test_arr_op_add(self):
        '''
        a = [1, 2, 3]
        a[1] += 10
        b = a[1]
        '''
        assert self.vm.frame.hash['b'] == 12

    def test_arr_op_sub(self):
        '''
        a = [1, 2, 3]
        a[1] -= 1
        b = a[1]
        '''
        assert self.vm.frame.hash['b'] == 1

    def test_arr_op_mul(self):
        '''
        a = [1, 2, 3]
        a[1] *= 2
        b = a[1]
        '''
        assert self.vm.frame.hash['b'] == 4

    def test_arr_op_div(self):
        '''
        a = [1, 20, 3]
        a[1] /= 4
        b = a[1]
        '''
        assert self.vm.frame.hash['b'] == 5

    def test_arr_op_fn(self):
        '''
        a = [1, 2, 3]

        fn1 = fn() do
            @a[0] = 100
        end

        fn1()

        b = a[0]
        '''
        assert self.vm.frame.hash['b'] == 100
