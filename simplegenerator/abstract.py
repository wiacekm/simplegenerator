# -*- coding: utf-8 -*-
"""This is module for abstract classes"""
import json
import yaml


class AbstractGenerator(object):
    """Abstract Generator class"""

    def __init__(self):
        raise NotImplementedError("Cannot initalize abstract class")

    def generate(self):
        raise NotImplementedError("generate method should be implemented")

    def to_json(self):
        """Generates data from model.

        Returns:
            data serialized to json
        """
        return json.dumps(self.generate())

    def to_yaml(self):
        """Generates data from model.

        Returns:
            data serialized to yaml
        """
        return yaml.dump(self.generate())

    def serialize(self, format=None):
        """generate and serialize addcording to format.

        Args:
            format (str): supports two options: json, yaml
                Default to None. When None there is no serialization at all.
        Returns:
            generated data serialized correctly
        """
        if format == 'json':
            return self.to_json()
        elif format == 'yaml':
            return self.to_yaml()
        elif format is None:
            return self.generate()
        else:
            raise ValueError("format not supported. We support json and yaml only")
