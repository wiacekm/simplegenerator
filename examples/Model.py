#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example model that shows how to implement credentials models"""
from models import (ModelBasedGenerator, Field,
                    PGenerator,
                    )
from keys import RSAKey


class PasswordWithRSAKey(ModelBasedGenerator):
    """Really simple password and RSA key model"""
    password = Field('[A-Za-z0-9]{10}')
    keys = RSAKey()


class BasicCredentials(ModelBasedGenerator):
    """Really simple user credentials with password and RSA Keys"""
    user = Field('(michal|user|root)[0-9]{2}')
    credentials = PasswordWithRSAKey()


class RSAKeyEncryptedWithGeneratedPassword(ModelBasedGenerator):
    """This RSA Key is encrypted with auto-generated password"""
    keys = RSAKey(password=PGenerator('[a-zA-Z0-9]'))
