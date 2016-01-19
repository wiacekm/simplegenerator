# -*- coding: utf-8 -*-
"""String hashing module

This module containts various methods to create string hashes.
It is based on python mosules that are already avaialble

"""
import os
from Crypto.PublicKey import RSA
import ecdsa
from .abstract import AbstractGenerator


class RSAKey(AbstractGenerator):
    """RSA Key generation class.

    This is class used to generate RSA SSH key pairs.

    Args:
        password (str): password used to encrypt private key
        bits (int): number of bits of generated hash
    """

    def __init__(self, password=None, bits=2048):
        self._password = password
        self._bits = bits

    def generate(self):
        """generate key pairs.

        Returns:
            Dictionary with private public keys and password
        """
        key = RSA.generate(self._bits, os.urandom)
        return {'private': key.exportKey(passphrase=self._password),
                'public': key.publickey().exportKey(),
                'password': self._password
                }


class ECDSAKey(AbstractGenerator):
    """ECDSA Key generation class.

    This is class used to generate ECDSA SSH key pairs.

    Args:
        curve (str): type of elliptic curve used for key generation
            (default=ecdsa.NIST384p)
    """

    def __init__(self, curve=ecdsa.NIST384p):
        self._curve = curve

    def generate(self):
        """generate key pairs.

        Returns:
            Dictionary with private public keys
        """
        sk = ecdsa.SigningKey.generate(self._curve)
        vk = sk.get_verifying_key()
        result = {'private': sk.to_pem(), 'public': vk.to_pem()}
        return result
