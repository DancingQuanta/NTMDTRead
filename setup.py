#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
	'pint'
]

setup(
    name='NTMDTRead',
    version='0.1.0',
    packages=['NTMDTRead'],
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ])
