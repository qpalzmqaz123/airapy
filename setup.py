#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

setup(
    name='aira',
    version='0.0.12',
    description='ruff auto flash',
    author='wangqj',
    author_email='wangqinjun@nanchao.org',
    url='http://git.nanchao.org:3000/wangqj/auto_flash.git',
    py_modules=['ruff_auto_flash'],
    scripts=['ruff_auto_flash.py'],
    install_requires=[
        'pyserial',
        'click',
        'termcolor'
    ])
