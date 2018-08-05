#!/usr/bin/env python3
# coding: utf-8

from .base import BaseTest

class TestHash(BaseTest):

    def test_hash_empty(self):
        '''
        a = {}
        '''
        assert self.vm.frame.hash['a']

    def test_hash_empty_set(self):
        '''
        a = {}
        a.k1 = 1
        a['k2'] = 2

        b = a['k1']
        c = a.k2
        '''
        assert self.vm.frame.hash['a']
        assert self.vm.frame.hash['b'] == 1
        assert self.vm.frame.hash['c'] == 2

    def test_hash_1(self):
        '''
        a = {'key': 'value'}
        b = a.key
        '''
        assert self.vm.frame.hash['a']
        assert self.vm.frame.hash['b'] == 'value'

    def test_hash_2(self):
        '''
        a = {'k1': 1, 'k2': 2}
        b = a.k1
        c = a.k2
        '''
        assert self.vm.frame.hash['a']
        assert self.vm.frame.hash['b'] == 1
        assert self.vm.frame.hash['c'] == 2
