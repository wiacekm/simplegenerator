#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = ['click==6.2',
                'pyparsing==2.0.7',
                'ecdsa==0.13',
                'PyYAML==3.11',
                'pycrypto==2.6.1',
                ]

config = {
    'name': 'SimpleGenerator',
    'description': 'Simple string (password) generator script',
    'author': 'Michal Wiacek',
    'author_email': 'michal.wiacek@gmail.com',
    'version': '0.1',
    'install_requires': requirements,
    'packages': ['simplegenerator'],
    'entry_points': {
        "console_scripts": [
            "pgen = simplegenerator.__main__:cli",
        ]
    }
}

setup(**config)
