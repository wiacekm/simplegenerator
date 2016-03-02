#!/usr/bin/env python
# -*- coding: utf-8 -*-
from simplegenerator import (alpha_lower, alpha_upper, numbers, space, underscore,
                             minus, special_characters, brackets,
                             SimpleGenerator,
                             )
import unittest


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
        with self.assertRaises(ValueError):
            SimpleGenerator(5, with_lower=False, with_upper=False,
                            withnumbers=False, withspace=False,
                            withunderscore=False, withminus=False,
                            withspecial_characters=False,
                            withbrackets=False)

    def zero_lengtht_string_test(self):
        with self.assertRaises(ValueError):
            SimpleGenerator(0, with_lower=True, with_upper=True,
                            withnumbers=True, withspace=True,
                            withunderscore=True, withminus=True,
                            withspecial_characters=True,
                            withbrackets=True)

    def all_groups_selected_test(self):
        test_generator = SimpleGenerator(1, with_lower=True, with_upper=True,
                                         withnumbers=True, withspace=True,
                                         withunderscore=True, withminus=True,
                                         withspecial_characters=True,
                                         withbrackets=True)
        result = test_generator.generate()
        self.assertEqual(len(result), 1)
        expected_pattern = ''.join([alpha_lower, alpha_upper,
                                    numbers, space, underscore, minus,
                                    special_characters, brackets
                                    ])
        self.assertTrue(result in expected_pattern)
