# -*- coding: utf-8 -*-
"""String (Password) generation module

This module contain classes with classes that generates string based on various methods.
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
import random
import string

from abstract import AbstractGenerator

__all__ = ['alpha_lower', 'alpha_upper', 'numbers', 'space', 'underscore',
           'minus', 'special_characters', 'brackets',
           'BaseGenerator', 'SimpleGenerator',
           ]

alpha_lower = string.ascii_lowercase
alpha_upper = string.ascii_uppercase
numbers = "0123456789"
space = " "
underscore = "_"
minus = "-"
special_characters = "`~!@#$%^&*+=,./?;':\|\""
brackets = "{}[]()<>"


class BaseGenerator(AbstractGenerator):
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

    def generate(self, length=None):
        """Method to generate/generate string

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
            raise ValueError("at least one group should be selected")
        elif not length > 0:
            raise ValueError("length should be greater than zero")

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
