#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyparsing import ParseFatalException
from simplegenerator import ReGenerator
import unittest


class ReGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.alphanum_pattern = "[a-zA-Z0-9_]"
        self.alpha_pattern = "[a-zA-Z]"
        self.num_pattern = "[0-9]"
        self.repeat_once = "{1}"
        self.repeat_nine_to_ten_times = "{9,10}"
        self.repeat_ten_times = "{10}"
        self.alternatives = "(abc|cde|efg)"
        self.alphanum_short_pattern = "\w"
        self.space_short_pattern = "\s"
        self.numbers_short_pattern = "\d"
        self.tabular_as_unsupported_character = "\t"
        self.unbounded_repetition_pattern = "*"
        self.repeat_once_question_mark = "?"

    def empty_pattern_test(self):
        with self.assertRaises(ValueError):
            ReGenerator("")

    def only_one_alphanum_character_test(self):
        test_gen = ReGenerator(self.alphanum_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.alphanum_pattern)
        self.assertRegexpMatches(result, self.alphanum_short_pattern)

    def space_short_pattern_test(self):
        test_gen = ReGenerator(self.space_short_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.space_short_pattern)
        self.assertRegexpMatches(result, ' ')

    def only_one_alphanum_shorthand_test(self):
        test_gen = ReGenerator(self.alphanum_short_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.alphanum_pattern)
        self.assertRegexpMatches(result, self.alphanum_short_pattern)

    def only_one_alphanum_character_when_length_is_specified_test(self):
        test_pattern = self.alphanum_pattern + self.repeat_once
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.alphanum_pattern)
        self.assertRegexpMatches(result, self.alphanum_short_pattern)

    def short_num_character_without_repeatition_test(self):
        test_gen = ReGenerator(self.numbers_short_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.numbers_short_pattern)
        self.assertRegexpMatches(result, self.num_pattern)

    def short_num_character_repeated_ten_times_test(self):
        test_pattern = self.numbers_short_pattern + self.repeat_ten_times
        equivalent_pattern = self.num_pattern + self.repeat_ten_times
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 10)
        self.assertRegexpMatches(result, test_pattern)
        self.assertRegexpMatches(result, equivalent_pattern)

    def alphanum_character_when_repeated_once_test(self):
        test_pattern = self.alphanum_pattern + self.repeat_once
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 1)
        self.assertRegexpMatches(result, self.alphanum_pattern)
        self.assertRegexpMatches(result, self.alphanum_short_pattern)

    def ten_alphanum_characters_when_length_is_specified_test(self):
        test_pattern = self.alphanum_pattern + self.repeat_ten_times
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 10)
        self.assertRegexpMatches(result, self.alphanum_pattern)
        self.assertRegexpMatches(result, self.alphanum_short_pattern)

    def variable_string_length_with_alpha_characters_test(self):
        test_pattern = self.alpha_pattern + self.repeat_nine_to_ten_times
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertGreaterEqual(len(result), 9)
        self.assertLessEqual(len(result), 10)
        self.assertRegexpMatches(result, self.alpha_pattern)
        self.assertNotRegexpMatches(result, self.num_pattern)

    def three_characters_alternatives_without_repetitions_test(self):
        test_gen = ReGenerator(self.alternatives)
        result = test_gen.generate()
        self.assertEqual(len(result), 3)
        self.assertRegexpMatches(result, self.alternatives)

    def three_characters_alternatives_repeated_ten_times(self):
        test_pattern = self.alternatives + self.repeat_ten_times
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 3 * 10)
        self.assertRegexpMatches(result, test_pattern)

    def string_reprezentation_of_pgenerator_test(self):
        test_pattern = self.alternatives + self.repeat_ten_times
        test_gen = ReGenerator(test_pattern)
        self.assertEqual(str(test_gen), "pattern: %s\n" % (test_pattern))
        self.assertEqual(repr(test_gen), "pattern: %s\n" % (test_pattern))

    def dot_as_pattern_test(self):
        test_pattern = '.'
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertRegexpMatches(result, '.')

    def unbounded_repetition_pattern_test(self):
        test_pattern = self.alpha_pattern + self.unbounded_repetition_pattern
        test_gen = ReGenerator(test_pattern)
        with self.assertRaises(ParseFatalException):
            test_gen.generate()

    def question_mark_as_repeat_once_pattern_test(self):
        test_pattern = self.alternatives + self.repeat_once_question_mark
        equivalent_pattern = self.alternatives + '{2}'
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertRegexpMatches(result, equivalent_pattern)
        self.assertEqual(len(result), 2 * 3)

    def alternative_from_characters_sequence_test(self):
        test_pattern = '([A-Z]{2}|[a-z]{2}|\d{2})'
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertRegexpMatches(result, test_pattern)
        self.assertEqual(len(result), 2)

    def unsupported_macro_character(self):
        test_gen = ReGenerator(self.tabular_as_unsupported_character)
        with self.assertRaises(ParseFatalException):
            test_gen.generate()

    def listerals_characters_test(self):
        test_pattern = 'test_literal'
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertEqual(result, test_pattern)

    def listerals_and_patterns_test(self):
        literal = 'test_literal'
        pattern = '[a-zA-Z0-9]{3}'
        test_pattern = literal + pattern
        test_gen = ReGenerator(test_pattern)
        result = test_gen.generate()
        self.assertEqual(len(result), 15)
        self.assertEqual(result[:12], literal)
        self.assertRegexpMatches(result[-3:], pattern)
