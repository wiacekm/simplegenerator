#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example model that shows how to implement credentials models"""
from models import (ModelBasedGenerator, Field)
from keys import RSAKey

class PasswordWithRSAKey(ModelBasedGenerator):
    """Really simple password and RSA key model"""
    password = Field('[a-z]{2}')
    keys = RSAKey()


class BasicCredentials(ModelBasedGenerator):
    """Really simple user credentials with password and RSA Keys"""
    user = Field('[a-z]{2}')
    credentials = PasswordWithRSAKey()
