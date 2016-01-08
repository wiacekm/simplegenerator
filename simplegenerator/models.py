#!/usr/bin/env python2


class Model(object):
    pass


class InvalidModelException(Exception):
    pass


class Field(object):

    def __init__(self, name, pattern, length):
        self._pattern = pattern
        self._length = length
        self._name = name

    def __str__(self):
        return "name: %s\npattern: %s\nlength: %s" % (self._name,
                                                      self._pattern,
                                                      self._length)

    __repr__ = __str__

    def build(self):
        pass
