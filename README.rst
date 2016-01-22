Simple (Password) Generator
===========================
.. image:: http://img.shields.io/travis/michalwiacek/simplegenerator.svg?branch=master
    :target: https://travis-ci.org/michalwiacek/simplegenerator.svg?branch=master
    :alt: Build status
.. image:: http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat
    :target: http://mit-license.org/
    :alt: License

This is ver simple python tool to generate strings ex. for passwords.
There are three possible options:

1. Build random string based on characters groups
#. Build random string based on regex-like patterns.Supported special characters:

    +-----------+------------------------------------------+----------------------------+ 
    | Character | Description                              | Example                    | 
    +===========+==========================================+============================+ 
    | \{}()|-.  | Restricted meta-characters.              |                            | 
    +-----------+------------------------------------------+----------------------------+ 
    | \         | Backslash escapes a metacharacter.       | column 3                   | 
    +-----------+------------------------------------------+----------------------------+ 
    | \d        | Digits shorthand.                        | exapnded to 0-9            | 
    +-----------+------------------------------------------+----------------------------+ 
    | \w        | Number shorthand.                        | expanded to ``A-Za-z0-9_`` | 
    +-----------+------------------------------------------+----------------------------+ 
    | \s        | Space shorthand.                         | expanded to (space) only   | 
    +-----------+------------------------------------------+----------------------------+ 
    | []        | Nested characters class.                 | ``[Abc_]``                 | 
    +-----------+------------------------------------------+----------------------------+ 
    | -         | Characters range (between to chars).     | ``[a-z]``, ``[A-Za-z0-9]`` | 
    +-----------+------------------------------------------+----------------------------+ 
    | {n}       | Reapat (random character) n-times.       | {5}                        | 
    +-----------+------------------------------------------+----------------------------+ 
    | {n,m}     | Repeat (random character) k-times,       |  {1,5}                     |
    |           | where k is random number form n-m range. |                            | 
    +-----------+------------------------------------------+----------------------------+ 
    | (a|b)     | random element from group.               | (user|root)                | 
    +-----------+------------------------------------------+----------------------------+ 

#. Generate Encryption keys:

    * RSA
    * ECDSA

#. Build random string or set of string based on predefined models. This models are build upon above generators.
   Models can be build as python class or as a YAML configuration file.
#. Results can be serialized to either json or yaml.
#. Simple comman line interface.

Usage Examples
==============

1. Simple Generator:

.. code-block:: python

    from simplegenerator import SimpleGenerator
    generator = SimpleGenerator(10, with_brackets=True)
    result1 = generator.generate()
    result2 = generator.generate(15)

#. Pattern Generator:

.. code-block:: python

    from simplegenerator import PGenerator
    pgenerator = PGenerator("[a-zA-Z0-9]{5-15}")
    result = pgenerator.generate()

#. Model based Generator:

.. code-block:: python

    from simplegenerator import (ModelBasedGenerator, Field, 
                                 RSAKey, PGenerator)
    
    class Model(ModelBasedGenerator):
        user = Field('[a-zA-Z]{10}')
        key = RSAKey(password=PGenerator('[a-zA-Z0-9]{15}')
    model_generator = Model()
    result = model_generator.generate()
    
#. Model Load from YAML file:

.. code-block:: yaml

    user:
        type: Field
        args:
            pattern: '[a-z]{2}'

            
.. code-block:: python

    from simplegenerator import ModelBasedGenerator
    
    generator = ModelBasedGenerator.load('model.yml')
    result = generator.generate()

More complex models can be find in examples folder.

Commandline scripts
===================
This tools provides also command line interface.

.. code-block:: shell

    $ simplegenerator simple --length 10 --with-lower --with-upper --with-numbers
    $ simplegenerator pattern --pattern [a-zA-Z0-9]{15}
    $ simplegenerator model --file model.yml

Issues
======

1. Problem with handling comples patterns ex. ``([A-Z]{2}|[a-z]{2})``
#. Problem with handling literals in patterns ex. ``michal[0-9]{3}``
