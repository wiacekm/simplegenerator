Simple (Password) Generator
===========================
.. image:: http://img.shields.io/travis/michalwiacek/simplegenerator.svg?branch=master
    :target: https://travis-ci.org/michalwiacek/simplegenerator.svg?branch=master
    :alt: Build status
.. image:: http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat
    :target: http://mit-license.org/
    :alt: License
.. image:: http://codecov.io/github/michalwiacek/simplegenerator/simplegenerator.svg?branch=master
    :target: http://codecov.io/github/michalwiacek/simplegenerator?branch=master
    :alt: Coverage

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

#. RegEx-like Generator:

.. code-block:: python

    from simplegenerator import ReGenerator
    pgenerator = ReGenerator("[a-zA-Z0-9]{5-15}")
    result = pgenerator.generate()

#. Model based Generator:

.. code-block:: python

    from simplegenerator import (ModelBasedGenerator, RegexField,
                                 StringField, RSAKey)

    class Model(ModelBasedGenerator):
        user = RegexField('[a-zA-Z]{10}')
        key = RSAKey(password=PGenerator('[a-zA-Z0-9]{15}')
        url = StringField('http://github.com/')

    model_generator = Model()
    result = model_generator.generate()

#. Model Load from YAML file:

.. code-block:: yaml

    user:
        type: RegexField
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
    $ simplegenerator regex --pattern [a-zA-Z0-9]{15}
    $ simplegenerator model --file model.yml

