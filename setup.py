#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import re


requirements = [i.strip() for i in open("requirements.txt").readlines()]

with open('simplegenerator/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r') as f:
    readme = f.read()

config = {
    'name': 'SimpleGenerator',
    'description': 'Simple string (password) generator script',
    'long_description': readme,
    'author': 'Michal Wiacek',
    'author_email': 'michal.wiacek@gmail.com',
    'version': version,
    'install_requires': requirements,
    'packages': ['simplegenerator'],
    'entry_points': {
        "console_scripts": [
            "pgen = simplegenerator.__main__:cli",
        ]
    },
    'classifiers': [
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
}

setup(**config)
