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
import yaml
from .abstract import AbstractGenerator
from .pgenerator import PGenerator

__all__ = ['ModelBasedGenerator', 'Field']

Field = PGenerator


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


class ModelBasedGenerator(AbstractGenerator):
    """Model Besed Generator base class.

    Example:

        $ class MyModel(ModelBasedGenerator):
        $     name = Field("[a-z]{3}")
        $ data = MyModel().generate()
        $ class MyNestedModel(ModelBasedGenerator):
        $     name = MyModel()
        $ data = MyNestedModel().to_json()

    This class is used to create models based on which
    set of random string will be created
    """

    __metaclass__ = ModelMeta

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
    def _extract(cls, kwargs):
        params = {}
        for name, value in kwargs.iteritems():
            if value['type'] == 'Model':
                params[name] = cls._extract(value['args'])
            else:
                params[name] = eval(value['type'])(**value['args'])
        return ModelBasedGenerator(**params)

    @classmethod
    def load(cls, file_name):
        with open(file_name, 'r') as fp:
            model = yaml.load(fp)
        return cls._extract(model)
