# -*- coding: utf-8 -*-
"""String (Password) generation module

This module contain classes with classes that generates string based on pattern.
It is based on python ``random`` package.

Example:
    This are some examples of how it can be used::

        $ regen = ReGenerator("[a-zA-Z0-9]{3-5}")
        $ result = regen.generate()

    Supports:
     - {n} and {m,n} repetition, but not unbounded + or * repetition
     - ? optional elements
     - [] character ranges
     - () grouping
     - | alternation

    there is also support for:
     - . (dot) any printable character
     - \s - change to space only
     - \w - equivalent to [A-Za-z0-9_]
     - \d - equivalent to [0-9]
     - all special characters can be escaped with \

    This package is very based on invRegex.py examples from pyparsing examples

"""
import random
from pyparsing import (Literal, oneOf, printables, ParserElement, Combine,
                       SkipTo, operatorPrecedence, ParseFatalException,
                       Word, nums, opAssoc,
                       Suppress, srange)
from abstract import AbstractGenerator


__all__ = ['ReGenerator', 'parser', 'Randomizer']


class Range(object):
    """This is class used to simplify creating random value from range

    This string is generated based on list of provided characters
    with desired length

    Args:
        min (int): lower boundary of range
        max (int): upper boundary of range
    """

    def __init__(self, min, max):
        self._min = min
        self._max = max

    @property
    def generate(self):
        """get random vlaue from range"""
        if self._min == self._max:
            return self._min
        else:
            return random.randrange(*self.range)

    @property
    def min(self):
        """set lower boundary"""
        return self._min

    @min.setter
    def min(self, min):
        """set lower boundary"""
        self._min = min

    @property
    def max(self):
        """get upper boundary"""
        return self._max

    @max.setter
    def max(self, max):
        """set upper boundary"""
        self._max = max

    @property
    def range(self):
        """Get range as a tuple"""
        return (self._min, self._max)

    def __str__(self):
        return '(%s,%s)' % (self._min, self._max)

    __repr__ = __str__


class CharSetRandomizer(object):
    """This to simplify charset generation

    This class is used to generate random charset based on provided:
     - chars
     - repetition range
    By default only one character will be generated
    what can be modified with additional methods

    Args:
        chars (List[str]): lower boundary of range
    """

    def __init__(self, chars):
        self._chars = chars
        self._count = Range(1, 1)

    def range(self, min, max):
        """set repetition range"""
        self._count.min = min
        self._count.max = max

    def count(self, count):
        """set repetition count"""
        self._count.min = count
        self._count.max = count

    def generate(self):
        """Generator which creates random length string with random characters

        Yields:
            Random characters

        """
        length = len(self._chars)
        for _ in xrange(self._count.generate):
            yield self._chars[random.randrange(length)]

    def __str__(self):
        return '{chars: %s,\n range: %s}' % (self._chars, self._count)

    __repr__ = __str__


class Randomizer(object):
    """Create string from list of CharSetRandomizer objects

    Args:
        charsets (List[CharSetRandomizer]): list based on which random strings can be created
    """
    def __init__(self, charsets):
        self._charsets = charsets

    def generate(self):
        """Generator based on CharSetRandomizer object list

        Yields:
            Random character
        """
        for charset in self._charsets:
            for char in charset.generate():
                yield char


def handleRange(toks):
    return CharSetRandomizer(srange(toks[0]))


def handleRepetition(toks):
    toks = toks[0]
    if toks[1] in "*+":
        raise ParseFatalException("", 0, "unbounded repetition operators not supported")
    if toks[1] == "?":
        toks[0].count(2)
    if "count" in toks:
        toks[0].count(int(toks.count))
    if "minCount" in toks:
        toks[0].range(int(toks.minCount), int(toks.maxCount))
    return toks[0]


def handleLiteral(toks):
    lit = ""
    for t in toks:
        if t[0] == "\\":
            if t[1] == "t":
                lit += '\t'
            else:
                lit += t[1]
        else:
            lit += t
    return lit


def handleMacro(toks):
    macroChar = toks[0][1]
    if macroChar == "d":
        return CharSetRandomizer(srange("[0-9]"))
    elif macroChar == "w":
        return CharSetRandomizer(srange("[A-Za-z0-9_]"))
    elif macroChar == "s":
        return CharSetRandomizer(" ")
    else:
        raise ParseFatalException("", 0, "unsupported macro character (" + macroChar + ")")


def handleSequence(toks):
    toks = toks[0]
    if any([isinstance(tok, CharSetRandomizer) for tok in toks]):
        return toks
    else:
        return ''.join(toks)


def handleDot():
    return CharSetRandomizer(printables)


def handleAlternative(toks):
    return CharSetRandomizer(toks[0])


_parser = None


def parser():
    """creates parser if not yet created

    Returns
        parser based on pyparsing package
    """
    global _parser
    if _parser is None:
        ParserElement.setDefaultWhitespaceChars("")
        lbrack, rbrack, lbrace, rbrace, lparen, rparen = map(Literal, "[]{}()")

        reMacro = Combine("\\" + oneOf(list("dws")))
        escapedChar = ~reMacro + Combine("\\" + oneOf(list(printables)))
        reLiteralChar = "".join(c for c in printables if c not in r"\[]{}().*?+|") + " \t"

        reRange = Combine(lbrack + SkipTo(rbrack, ignore=escapedChar) + rbrack)
        reLiteral = (escapedChar | oneOf(list(reLiteralChar)))
        reDot = Literal(".")
        repetition = (
            (lbrace + Word(nums).setResultsName("count") + rbrace) |
            (lbrace + Word(nums).setResultsName("minCount") + "," + Word(nums).setResultsName("maxCount") + rbrace) |
            oneOf(list("*+?"))
            )

        reRange.setParseAction(handleRange)
        reLiteral.setParseAction(handleLiteral)
        reMacro.setParseAction(handleMacro)
        reDot.setParseAction(handleDot)

        reTerm = (reLiteral | reRange | reMacro | reDot)
        reExpr = operatorPrecedence(reTerm, [
                                    (repetition, 1, opAssoc.LEFT, handleRepetition),
                                    (None, 2, opAssoc.LEFT, handleSequence),
                                    (Suppress('|'), 2, opAssoc.LEFT, handleAlternative),
                                    ]
                                    )
        _parser = reExpr

    return _parser


class ReGenerator(AbstractGenerator):
    """Regex-like Pattern Generator

    This generator uses regex-like patterns to generate random string
    which can be used as a random password or username

    Args:
        pattern (str): pattern used to generate string

    """

    def __init__(self, pattern):
        if not pattern:
            raise ValueError("Pattern cannot be empty")
        self._pattern = pattern
        self._parser = parser()

    def __str__(self):
        return "pattern: %s\n" % (self._pattern)

    __repr__ = __str__

    def igenerate(self):
        """random characters generator

        Yields:
            random character
        """
        for c in Randomizer(self._parser.parseString(self._pattern)).generate():
            yield c

    def generate(self):
        """generate random string

        Returns:
            generated string
        """
        return ''.join([c for c in self.igenerate()])
