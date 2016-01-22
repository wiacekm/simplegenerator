#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from simplegenerator import AbstractGenerator


class InvalidGenerator(AbstractGenerator):

    def __init__(self):
        pass


class GeneratorTest(unittest.TestCase):

    def instantiatig_abtract_generator_test(self):
        with self.assertRaises(NotImplementedError):
            AbstractGenerator()

    def using_invalid_generator_test(self):
        generator = InvalidGenerator()
        with self.assertRaises(NotImplementedError):
            generator.generate()
