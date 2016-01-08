# -*- coding: utf-8 -*-
"""String (Password) generation module

This module contain classes with classes that generates string based on various methods.
It is based on python ``random`` package.

Example:
    This are some examples of how it can be used::

        $ base_gen = BaseGenerator(10, ['a', 'b', 'c'])
        $ result1 = base_gen.build()
        $ result2 = base_gen.build(2)

        $ simple_gen = SimpleGenerator()
        $ result3 = simple_gen.build()
        $ result4 = simple_gen.build(5)

        $ pattern_gen = PatternGenerator("[a-zA-Z0-9]{3-5}")
        $ result5 = pattern_gen.build()

"""
import random
import string

__all__ = ['alpha_lower', 'alpha_upper', 'numbers', 'space', 'underscore',
           'minus', 'special_characters', 'brackets',
           'BaseGenerator', 'SimpleGenerator', 'PatternGenerator',
           'CompilationError', 'InvalidGeneratorValueError'
           ]

alpha_lower = string.ascii_lowercase
alpha_upper = string.ascii_uppercase
numbers = "0123456789"
space = " "
underscore = "_"
minus = "-"
special_characters = "`~!@#$%^&*+=,./?;':\|\""
brackets = "{}[]()<>"


class BaseGenerator(object):
    """This is base generator which creates random string.

    This string is generated based on list of provided characters
    with desired length

    Args:
        length (int): length of generated string
        selectable_characters (List[str]): list of prefered characters
    """

    def __init__(self, length, selectable_characters):
        self._selectable_characters = selectable_characters
        self._length = length

    def build(self, length=None):
        """Method to build/generate string

        Args:
            length (Optional[int]): lentgh of the string. Defaults to None.
                If not provided class attribute is used

        Returns:
            Generated string
        """
        if length is None:
            length = self._length
        self._selectable_chars_list_length = len(self._selectable_characters)
        character_list = [self._selectable_characters[random.randrange(self._selectable_chars_list_length)]
                          for _
                          in xrange(length)]
        random.shuffle(character_list)
        return ''.join(character_list)


class SimpleGenerator(BaseGenerator):
    """This is simple generators where you select characters groups based on flags provided

    Args:
        length (int): length of generated string
        with_lower (Optional[bool]): if True lower-case alpha-characters are included.
            Defaults to True.
        with_upper (Optional[bool]): if True upper-case alpha-characters are included.
            Defaults to True.
        withnumbers (Optional[bool]): if True numbers are included.
            Defaults to True.
        withspace (Optional[bool]): if True space is included.
            Defaults to False.
        withunderscore (Optional[bool]): if True underscore is included.
            Defaults to False.
        withminus (Optional[bool]): if True minus is included.
            Defaults to False.
        withspecial_characters (Optional[bool]): if True special characters are included.
            Defaults to False.
        withbrackets (Optional[bool]): if True brackets are included.
            Defaults to False.

    """

    def __init__(self, length,
                 with_lower=True, with_upper=True, withnumbers=True,
                 withspace=False, withunderscore=False, withminus=False,
                 withspecial_characters=False, withbrackets=False):

        if not any([with_lower, with_upper, withnumbers, withspace,
                    withunderscore, withminus,
                    withspecial_characters, withbrackets]):
            raise InvalidGeneratorValueError("at least one group should be selected")
        if not length > 0:
            raise InvalidGeneratorValueError("length should be greater than zero")

        selectable_characters = []
        if with_lower:
            selectable_characters.extend(list(alpha_lower))
        if with_upper:
            selectable_characters.extend(list(alpha_upper))
        if withnumbers:
            selectable_characters.extend(list(numbers))
        if withspace:
            selectable_characters.extend(list(space))
        if withunderscore:
            selectable_characters.extend(list(underscore))
        if withminus:
            selectable_characters.extend(list(minus))
        if withspecial_characters:
            selectable_characters.extend(list(special_characters))
        if withbrackets:
            selectable_characters.extend(list(brackets))
        random.shuffle(selectable_characters)
        super(SimpleGenerator, self).__init__(length, selectable_characters)


_normal_sequences = {'a-z': alpha_lower,
                     'A-Z': alpha_upper,
                     '0-9': numbers,
                     '\w': alpha_lower+alpha_upper+numbers,
                     '\s': space,
                     '\d': numbers}


class PatternGenerator(object):
    """This generator build string based on regexp-like pattern

    Args:
        pattern (str): This is regexp like pattern
            supported syntax
            [] - brackets for listing characters where we can put sequences
            or single values
            a-z,A-Z,0-9 - character sequences
            {n} - repeat count
            {n,m} - random repeat count from range n-m
    """

    def __init__(self, pattern):
        if not pattern:
            raise InvalidGeneratorValueError("Pattern cannot be empty")
        self._pattern = pattern
        self._compiled_sequence = []

    def _compile(self):
        """Method to compile pattern to sequnce

        sequence is a list of tuples:
        (list_of_characters, min_repetition, max_repetition)
        or
        (list_of_characters, None, repetition_count)

        """
        values = []
        min = None
        max = 1
        i = 0
        add_sequence = False
        pattern = list(self._pattern)
        while i < len(pattern):
            key = pattern[i]
            if key == '[':
                i += 1
                while pattern[i] != ']':
                    values.append(pattern[i])
                    i += 1
                if i+1 >= len(pattern):
                    add_sequence = True
                elif pattern[i+1] != '{':
                    add_sequence = True
            if key == '\\':
                i += 1
                values.append(pattern[i])
                if i+1 >= len(pattern):
                    add_sequence = True
                elif pattern[i+1] != '{':
                    add_sequence = True
            elif key == '{':
                i += 1
                min = None
                current = []
                while pattern[i] != '}':
                    if pattern[i] == ',':
                        min = int(''.join(current))
                        current = []
                    else:
                        current.append(pattern[i])
                    i += 1
                max = int(''.join(current))
                add_sequence = True
            if add_sequence:
                add_sequence = False
                self._add_sequence(''.join(values), min, max)
                values = []
                min = None
                max = 1
            i += 1

    def _add_sequence(self, sequence, min, max):
        """Method that add sequence tuple to a list"""
        for key, value in _normal_sequences.iteritems():
            sequence = sequence.replace(key, value)
        sequence = list(set(sequence))
        random.shuffle(sequence)
        self._compiled_sequence.append((sequence, min, max))

    def build(self):
        """String build/generate methods

        Returns:
            Generated string
        """
        password = []
        self._compile()
        for sequence, min, max in self._compiled_sequence:
            if min is None:
                repeat_count = max
            else:
                repeat_count = random.randrange(min, max)
            length = len(sequence)
            temp = [sequence[random.randrange(length)]
                    for
                    _ in xrange(repeat_count)]
            random.shuffle(temp)
            password.extend(temp)
        return ''.join(password)


class CompilationError(ValueError):
    """This exception should be raised when Pattern is invalid"""
    pass


class InvalidGeneratorValueError(ValueError):
    """This exception should be raised when generator values are invalid"""
    pass
