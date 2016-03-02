#!/usr/bin/env python2
"""String (Password) generation module

This module contain classes with classes
that generates string based on various methods.
It is based on python ``random`` package.

Example:
    This are some examples of how it can be used::

        $ base_gen = BaseGenerator(10, ['a', 'b', 'c'])
        $ result1 = base_gen.generate()
        $ result2 = base_gen.generate(2)

        $ simple_gen = SimpleGenerator()
        $ result3 = simple_gen.generate()
        $ result4 = simple_gen.generate(5)

"""
from abstract import AbstractGenerator
from keys import (RSAKey, ECDSAKey)
from regenerator import ReGenerator
import six
import yaml

__all__ = ['ModelBasedGenerator', 'RegexField', 'StringField']

RegexField = ReGenerator


class StringField(AbstractGenerator):
    """Class that represent basic string field"""

    def __init__(self, value):
        self._value = value

    def generate(self):
        """generate method.

        Returns:
            return value
        """
        return self._value


class ModelMeta(type):
    """Model metaclass.

    Metclass to create Models correctly.
    It is done to support nested models
    and iteratio through fields
    """

    def __init__(self, name, bases, dct):
        self._fields = {key
                        for key, value
                        in dct.iteritems()
                        if isinstance(value, AbstractGenerator)}
        super(ModelMeta, self).__init__(name, bases, dct)


@six.add_metaclass(ModelMeta)
class ModelBasedGenerator(AbstractGenerator):
    """Model Besed Generator base class.

    Example:

        $ class MyModel(ModelBasedGenerator):
        $     name = RegexField("[a-z]{3}")
        $ data = MyModel().generate()
        $ class MyNestedModel(ModelBasedGenerator):
        $     name = MyModel()
        $ data = MyNestedModel().to_json()

    This class is used to create models based on which
    set of random string will be created
    """

    def __init__(self, **kwargs):
        for name, value in kwargs.iteritems():
            self.__setattr__(name, value)
        if kwargs:
            self._fields = set(kwargs.keys())

    def generate(self, type=None):
        """generate string from model.

        Returns:
            Disctionary with field name and generated string as value
        """
        return {field: getattr(self, field).generate() for field in self._fields}

    @classmethod
    def extract(cls, kwargs):
        """Use dictionary like serialized objects to generate models.

        Args:
            kwargs (dict): model in format of dictionary
                Dictionary like this:
                    $ model = {'user': {'type': 'RegexField',
                                         'args': { pattern: '[a-z]{2}'},
                              },
                Is equivalent to:
                    $ class ExampleModel(ModelBasedGenerator):
                    $     user = RegexField('[a-z]{2}')
        Returns:
            ModelBasedGenerator-like object.
        """

        params = {}
        for name, value in kwargs.iteritems():
            if value['type'] == 'Model':
                params[name] = cls.extract(value['args'])
            else:
                params[name] = eval(value['type'])(**value.get('args', {}))
        return ModelBasedGenerator(**params)

    @classmethod
    def load(cls, file_name):
        """Load models for YAML definiction file.

        Example file content should look like this:

            $ user:
            $     type: RegexField
            $     args:
            $         pattern: '[a-z]{2}'

        Args:
            file_name (str): file name with YAML model
        Returns:
            ModelBasedGenerator-like object.
        """
        with open(file_name, 'r') as fp:
            model = yaml.load(fp)
        return cls.extract(model)
