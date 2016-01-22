#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from simplegenerator import RSAKey
from simplegenerator import ECDSAKey


class PGeneratorTest(unittest.TestCase):

    def setUp(self):
        pass

    def basic_rsakey_test(self):
        rsa = RSAKey()
        rsa_dict = rsa.generate()
        self.assertTrue('private' in rsa_dict)
        self.assertTrue('public' in rsa_dict)
        self.assertTrue('password' in rsa_dict)
        self.assertTrue('BEGIN RSA PRIVATE KEY' in rsa_dict['private'])
        self.assertTrue('BEGIN PUBLIC KEY' in rsa_dict['public'])
        self.assertEqual(rsa_dict['password'], None)
        self.assertEqual(len(rsa_dict), 3)

    def basic_ecdsakey_test(self):
        ecdsa = ECDSAKey()
        ecdsa_dict = ecdsa.generate()
        self.assertTrue('private' in ecdsa_dict)
        self.assertTrue('public' in ecdsa_dict)
        self.assertTrue('BEGIN EC PRIVATE KEY' in ecdsa_dict['private'])
        self.assertTrue('BEGIN PUBLIC KEY' in ecdsa_dict['public'])
        self.assertEqual(len(ecdsa_dict), 2)

    def rsakey_with_password_test(self):
        rsa = RSAKey(password='abc')
        rsa_dict = rsa.generate()
        self.assertTrue('BEGIN RSA PRIVATE KEY' in rsa_dict['private'])
        self.assertTrue('BEGIN PUBLIC KEY' in rsa_dict['public'])
        self.assertEqual(rsa_dict['password'], 'abc')
        self.assertEqual(len(rsa_dict), 3)

    def rsakey_with_to_json_test(self):
        rsa = RSAKey(password='abc')
        rsa_json = rsa.to_json()
        self.assertEqual(type(rsa_json), str)

    def rsakey_with_to_yaml_test(self):
        rsa = RSAKey(password='abc')
        rsa_yaml = rsa.to_yaml()
        self.assertEqual(type(rsa_yaml), str)

    def ecdsakey_with_to_json_test(self):
        ecdsa = ECDSAKey()
        ecdsa_json = ecdsa.to_json()
        self.assertEqual(type(ecdsa_json), str)

    def ecdsakey_with_to_yaml_test(self):
        ecdsa = ECDSAKey()
        ecdsa_yaml = ecdsa.to_yaml()
        self.assertEqual(type(ecdsa_yaml), str)

    def ecdsakey_with_yaml_format_serialization_test(self):
        ecdsa = ECDSAKey()
        ecdsa_yaml = ecdsa.serialize('yaml')
        self.assertEqual(type(ecdsa_yaml), str)

    def ecdsakey_with_json_format_serialization_test(self):
        ecdsa = ECDSAKey()
        ecdsa_json = ecdsa.serialize('json')
        self.assertEqual(type(ecdsa_json), str)

    def ecdsakey_with_invalid_format_serialization_test(self):
        ecdsa = ECDSAKey()
        with self.assertRaises(ValueError):
            ecdsa.serialize('invalid')
