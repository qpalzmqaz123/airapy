#!/usr/bin/env python3
# coding: utf-8

from .base import BaseTest

class TestFn(BaseTest):

    def test_empty_args(self):
        '''
        fn1 = fn() do
            return 1
        end

        a = fn1()
        '''
        assert self.vm.frame.hash['a'] == 1

    def test_1_arg(self):
        '''
        fn1 = fn(v) do
            return v + 1
        end

        a = fn1(10)
        '''
        assert self.vm.frame.hash['a'] == 11

    def test_2_args(self):
        '''
        fn1 = fn(a, b) do
            return a + b
        end

        a = fn1(2, 3)
        '''
        assert self.vm.frame.hash['a'] == 5

    def test_3_args(self):
        '''
        fn1 = fn(a, b, c) do
            return a + b + c
        end

        a = fn1(2, 3, 4)
        '''
        assert self.vm.frame.hash['a'] == 9

    def test_without_return(self):
        '''
        fn1 = fn() do
        end

        a = fn1()
        '''
        assert self.vm.frame.hash['a'] == None

    def test_return_nil(self):
        '''
        fn1 = fn() do
            return
        end

        a = fn1()
        '''
        assert self.vm.frame.hash['a'] == None

    def test_read_global(self):
        '''
        g = 1

        fn1 = fn() do
            return g
        end

        a = fn1()
        '''
        assert self.vm.frame.hash['a'] == 1

    def test_set_global(self):
        '''
        g = 1

        fn1 = fn() do
            @g = 2
        end

        a = fn1()
        '''
        assert self.vm.frame.hash['g'] == 2

    def test_set_global_1(self):
        '''
        g = 1

        fn1 = fn() do
            @g += 2
        end

        a = fn1()
        '''
        assert self.vm.frame.hash['g'] == 3

    def test_closure(self):
        '''
        fn1 = fn(v) do
            cnt = 0

            return fn() do
                @cnt += v

                return cnt
            end
        end

        fn2 = fn1(10)

        a = fn2()
        b = fn2()
        c = fn2()
        '''
        assert self.vm.frame.hash['a'] == 10
        assert self.vm.frame.hash['b'] == 20
        assert self.vm.frame.hash['c'] == 30

    def test_call_anonymous_fn(self):
        '''
        a = 1

        fn(v) do
            @a = v
        end(100)
        '''
        assert self.vm.frame.hash['a'] == 100

    def test_fn_add(self):
        '''
        a = 1 + fn() do
            return 10
        end()
        '''
        assert self.vm.frame.hash['a'] == 11

    def test_recursive(self):
        '''
	sum = fn(from, to) do
	    if from == to do
		return to
	    end

	    return from + sum(from + 1, to)
	end

	a = sum(1, 100)
        '''
        assert self.vm.frame.hash['a'] == 5050
