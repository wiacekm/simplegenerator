#!/usr/bin/env python
# -*- coding: utf-8 -*-
from click.testing import CliRunner
from simplegenerator.__main__ import cli
import unittest


class CliGeneratorTests(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def simple_generator_cli_test(self):
        result = self.runner.invoke(cli, ['simple'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(result.output), 10+1)  # plus one as new line is counted

    def pattern_generator_cli_test(self):
        result = self.runner.invoke(cli, ['pattern', '--pattern', '[A-Za-z]{5}'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(result.output), 5+1)  # plus one as new line is counted
