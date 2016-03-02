#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
from simplegenerator import keys
from simplegenerator import models
import unittest


class ModelsTest(unittest.TestCase):

    def setUp(self):
        pass

    def simple_model_generator_test(self):
        class MyModel(models.ModelBasedGenerator):
            test = models.RegexField("[a]")

        model = MyModel()
        result = model.generate()
        self.assertEqual(type(result), dict)

    def model_with_rsakey_test(self):
        class MyModel(models.ModelBasedGenerator):
            test = models.RegexField("[a]")
            key = keys.RSAKey()
            url = models.StringField('http://github.com')

        model = MyModel()
        result = model.generate()
        self.assertEqual(type(result), dict)
        self.assertEqual(type(result['key']), dict)
        self.assertTrue('private' in result['key'])
        self.assertTrue('public' in result['key'])
        self.assertTrue('password' in result['key'])
        self.assertTrue('http://github.com' in result['url'])

    def model_definition_from_yaml_file_test(self):
        model_definition = ["---",
                            "a:",
                            "    type: RegexField",
                            "    args:",
                            "        pattern: '[a-z]{2}'",
                            "b:",
                            "    type: Model",
                            "    args:",
                            "        d:",
                            "            type: RegexField",
                            "            args:",
                            "                pattern: '[a-z]{2}'",
                            "        url:",
                            "            type: StringField",
                            "            args:",
                            "                value: 'http://github.com'",
                            ]

        m = mock.mock_open(read_data='\n'.join(model_definition))
        with mock.patch('simplegenerator.models.open', m):
            model = models.ModelBasedGenerator.load('test.yml')
        result = model.generate()
        self.assertEqual(type(result), dict)
        self.assertRegexpMatches(result['a'], '[a-z]{2}')
        self.assertEqual(type(result['b']), dict)
        self.assertRegexpMatches(result['b']['d'], '[a-z]{2}')
        self.assertEqual(result['b']['url'], 'http://github.com')
