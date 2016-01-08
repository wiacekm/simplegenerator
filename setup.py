#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

config = {
    'name': 'StringGenerator',
    'description': 'Simple string (password) generator script',
    'author': 'Michal Wiacek',
    'author_email': 'michal.wiacek@gmail.com',
    'version': '0.1',
    'install_requires': REQUIREMENTS,
    'packages': ['simplegenerator'],
    'entry_points': {
        "console_scripts": [
            "pgen = simplegenerator.__main__:cli",
        ]
    }
}

setup(**config)
