#!/usr/bin/env python3
# coding: utf-8

from .base import BaseTest

class TestException(BaseTest):

    def test_exception_0(self):
        '''
        a = 1
        b = 1

        try do
            a = 2
        catch err do
            a = 3
        end

        b = 10
        '''
        assert self.vm.frame.hash['a'] == 2
        assert self.vm.frame.hash['b'] == 10

    def test_exception_1(self):
        '''
        a = 1
        b = 1

        try do
            a = 2
            throw Error('abc')
        catch err do
            a = 3
        end

        b = 10
        '''
        assert self.vm.frame.hash['a'] == 3
        assert self.vm.frame.hash['b'] == 10
        assert self.vm.frame.hash['err'].message == 'abc'

    def test_exception_2(self):
        '''
        a = 1
        b = 1

        fn1 = fn() do
            try do
                @a = 2
                throw Error('abc')
            catch err do
                @a = 3
            end
        end

        fn1()

        b = 10
        '''
        assert self.vm.frame.hash['a'] == 3
        assert self.vm.frame.hash['b'] == 10

    def test_exception_3(self):
        '''
        a = 1
        b = 1

        fn1 = fn() do
            try do
                @a = 2
            catch err do
                @a = 3
            end
        end

        fn1()

        b = 10
        '''
        assert self.vm.frame.hash['a'] == 2
        assert self.vm.frame.hash['b'] == 10
