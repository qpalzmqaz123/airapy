#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

setup(
    name='aira',
    version='0.0.1',
    description='aira script language',
    author='wangqj',
    author_email='qpalzmqaz123@gmail.com',
    url='',
    packages=['aira'],
    scripts=['bin/aira'],
    install_requires=[
        'ply',
        'click'
    ])
