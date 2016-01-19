Simple String (Password) Generator
==============

This is ver simple python tool to generate string ex. passwords based on simple patterns or characters groups.
Patterns have regex-like syntax.
Supported special characters

* \ - escaping other special characters ex. \\, \[
* \d - digits
* \w - expanded to a-zA-Z0-9
* [] - brackets for literal or sequences
* - - used for sequences like A-Z, a-z, 0-9
* {n} - repeat n-times
* {n,m} - repeat n to m times. random number between n and m


Usage Example:

.. code-block:: python

    from simplegenerator import SimpleGenerator, PGenerator
    generator = SimpleGenerator(10, with_brackets=True)
    password = generator.build()
    passowrd2 = generator.build(15)
    pgenerator = PGenerator("[a-zA-Z0-9]{5-15}")
    passowrd3 - pgenerator.build()


This also creates command line scripts:


.. code-block:: shell

    $ simplegenerator generate
    $ simplegenerator generate_pattern
