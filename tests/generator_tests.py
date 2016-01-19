#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from simplegenerator import SimpleGenerator
from simplegenerator import InvalidGeneratorValueError


class GeneratorTest(unittest.TestCase):

    def setUp(self):
        self.alphanum_pattern = "[a-zA-Z0-9]"
        self.alpha_pattern = "[a-zA-Z]"

    def empty_pattern_test(self):
        test_generator = SimpleGenerator(5)
        result = test_generator.generate()
        self.assertEqual(len(result), 5)
        self.assertRegexpMatches(result, self.alphanum_pattern)

    def none_character_group_selected_test(self):
        with self.assertRaises(InvalidGeneratorValueError):
            SimpleGenerator(5, with_lower=False, with_upper=False,
                            withnumbers=False, withspace=False,
                            withunderscore=False, withminus=False,
                            withspecial_characters=False,
                            withbrackets=False)
