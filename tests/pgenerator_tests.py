#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from simplegenerator import PGenerator
from simplegenerator import InvalidGeneratorValueError


class PGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.alphanum_pattern = "[a-zA-Z0-9]"
        self.alpha_pattern = "[a-zA-Z]"
        self.num_pattern = "[0-9]"
        self.repeat_once = "{1}"
        self.repeat_nine_to_ten_times = "{9,10}"
        self.repeat_ten_times = "{10}"
        self.alternatives = "(abc|cde|efg)"
        self.alphanum_short_pattern = "\w"
        self.numbers_short_pattern = "\d"

    def empty_pattern_test(self):
        with self.assertRaises(InvalidGeneratorValueError):
            PGenerator("")

    def only_one_alphanum_character_test(self):
        test_gen = PGenerator(self.alphanum_pattern)
        result = test_gen.build()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.alphanum_pattern)
        self.assertRegexpMatches(result, self.alphanum_short_pattern)

    def only_one_alphanum_character_when_length_is_specified_test(self):
        test_gen = PGenerator(self.alphanum_pattern+self.repeat_once)
        result = test_gen.build()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.alphanum_pattern)
        self.assertRegexpMatches(result, self.alphanum_short_pattern)

    def short_num_character_without_repeatition_test(self):
        test_gen = PGenerator(self.numbers_short_pattern)
        result = test_gen.build()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.numbers_short_pattern)
        self.assertRegexpMatches(result, self.num_pattern)

    def short_num_character_repeated_ten_times_test(self):
        test_gen = PGenerator(self.numbers_short_pattern+self.repeat_ten_times)
        result = test_gen.build()
        self.assertEqual(len(result), 10)
        self.assertRegexpMatches(result, self.numbers_short_pattern+self.repeat_ten_times)
        self.assertRegexpMatches(result, self.num_pattern+self.repeat_ten_times)

    def alphanum_character_when_repeated_once_test(self):
        test_gen = PGenerator(self.alphanum_pattern+self.repeat_once)
        result = test_gen.build()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.alphanum_pattern)
        self.assertRegexpMatches(result, self.alphanum_short_pattern)

    def ten_alphanum_characters_when_length_is_specified_test(self):
        test_gen = PGenerator(self.alphanum_pattern+self.repeat_ten_times)
        result = test_gen.build()
        self.assertEqual(len(result), 10)
        self.assertRegexpMatches(result, self.alphanum_pattern)
        self.assertRegexpMatches(result, self.alphanum_short_pattern)

    def variable_string_length_with_alpha_characters_test(self):
        test_gen = PGenerator(self.alpha_pattern+self.repeat_nine_to_ten_times)
        result = test_gen.build()
        self.assertGreaterEqual(len(result), 9)
        self.assertLessEqual(len(result), 10)
        self.assertRegexpMatches(result, self.alpha_pattern)
        self.assertNotRegexpMatches(result, self.num_pattern)

    def three_characters_alternatives_without_repetitions_test(self):
        test_gen = PGenerator(self.alternatives)
        result = test_gen.build()
        self.assertEqual(len(result), 3)
        self.assertRegexpMatches(result, self.alternatives)

    def three_characters_alternatives_repeated_ten_times(self):
        test_pattern = self.alternatives+self.repeat_ten_times
        test_gen = PGenerator(test_pattern)
        result = test_gen.build()
        self.assertEqual(len(result), 3*10)
        self.assertRegexpMatches(result, test_pattern)
