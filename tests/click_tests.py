#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import mock
from click.testing import CliRunner
from simplegenerator.__main__ import cli


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

    def model_definition_from_yaml_file_test(self):
        model_definition = ["---",
                            "a:",
                            "    type: Field",
                            "    args:",
                            "        pattern: '[a-z]{2}'",
                            "b:",
                            "    type: Model",
                            "    args:",
                            "        d:",
                            "            type: Field",
                            "            args:",
                            "                pattern: '[a-z]{2}'",
                            ]

        m = mock.mock_open(read_data='\n'.join(model_definition))
        with mock.patch('simplegenerator.models.open', m):
            result = self.runner.invoke(cli, ['model', '--file', 'test.yml'])
        print result
        self.assertEqual(result.exit_code, 0)
