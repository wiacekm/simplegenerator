#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import tempfile
from simplegenerator import models
from simplegenerator import keys


class ModelsTest(unittest.TestCase):

    def setUp(self):
        pass

    def simple_model_generator_test(self):
        class MyModel(models.ModelBasedGenerator):
            test = models.Field("[a]")

        model = MyModel()
        result = model.generate()
        self.assertEqual(type(result), dict)

    def model_with_rsakey_test(self):
        class MyModel(models.ModelBasedGenerator):
            test = models.Field("[a]")
            key = keys.RSAKey()

        model = MyModel()
        result = model.generate()
        print model
        print result
        self.assertEqual(type(result), dict)
        self.assertEqual(type(result['key']), dict)
        self.assertTrue('private' in result['key'])
        self.assertTrue('public' in result['key'])
        self.assertTrue('password' in result['key'])

    def model_definition_from_yaml_file(self):
        model_definition = """---
a: 
    type: Field
    args: 
        pattern: '[a-z]{2}'
b:
    type: Model
    args:
        d: 
            type: Field
            args: 
                pattern: '[a-z]{2}'
"""
        model = models.ModelBasedGenerator.load(file_name)
        result = model.generate()
        self.assertEqual(type(result), dict)
        self.assertRegexpMatches(result['a'], '[a-z]{2}')
        self.assertEqual(type(result['b']), dict)
        self.assertRegexpMatches(result['b']['d'], '[a-z]{2}')
