#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic command line interface for generating strings

it supports two sub commands:

generate::

    $ python simplegenerator generate
    $ python simplegenerator generate --length 5 --with_special_characters

pgenerate::

    $ python simplegenerator pgenerate
    $ python simplegenerator pgenerate --pattern [a-zA-Z]{10}

"""
import generator
import models
import pgenerator
import click


@click.group()
def cli1():
    pass


@cli1.command()
@click.option("--pattern", default="[A-Ba-z0-9]{10,15}",
              help="Pattern for string created. Supports regexp limited syntax")
@click.option('--format', type=click.Choice(['json', 'yaml']), default=None)
def pattern(pattern, format):
    """RegExp-like pattern string generator.

    Supports regexp-like syntax.

    Args:
        pattern (str): RegExp-like pattern
            Supported sequences:
            [a-zA-Z0-9] -- one character from all alpha upper and lower case plus digits

            sequence repeating options:
            {n} - repeat n count
            {m,n} - random value from range <m,n>
        format (Optional[str]): type of format in which data should be returned
            Defaults to 'yaml'. Available choices: yaml, json

    """
    pattern_gen = pgenerator.PGenerator(pattern)
    click.echo(pattern_gen.serialize(format))


@click.group()
def cli2():
    pass


@cli2.command()
@click.option("--length", default=10, help="Lenght of of a string")
@click.option("--with-lower/--without-lower", is_flag=True, default=True,
              help="Use lower-case alpha-characters in string")
@click.option("--with-upper/--without-upper", is_flag=True, default=True,
              help="Use upper-case alpha-characters in string")
@click.option("--with-numbers/--without-numbers", is_flag=True, default=True,
              help="Use numbers in string")
@click.option("--with-space/--without-space", is_flag=True, default=False,
              help="Use space ( ) in string")
@click.option("--with-underscore/--without-underscore", is_flag=True, default=False,
              help="Use underscore (_) in string")
@click.option("--with-minus/--without-minus", is_flag=True, default=False,
              help="Use minus (-) in string")
@click.option("--with-special-characters/--without-special-characters",
              is_flag=True, default=False,
              help="Use special_characters (%s) in string" % generator.special_characters)
@click.option("--with-brackets/--without-brackets", is_flag=True, default=False,
              help="Use brackets (%s) in string" % generator.brackets)
@click.option('--format', type=click.Choice(['json', 'yaml']), default=None)
def simple(length, with_lower, with_upper, with_numbers,
           with_space, with_underscore, with_minus,
           with_special_characters,
           with_brackets, format):
    """Simple string generator.

    This is fairly simple method to generate string
    with specified length and specified characters groups

    Args:
        length (int): length of generated string
        with_lower (Optional[bool]): if True lower-case alpha-characters are included.
            Defaults to True.
        with_upper (Optional[bool]): if True upper-case alpha-characters are included.
            Defaults to True.
        with_numbers (Optional[bool]): if True numbers are included.
            Defaults to True.
        with_space (Optional[bool]): if True space is included.
            Defaults to False.
        with_underscore (Optional[bool]): if True underscore is included.
            Defaults to False.
        with_minus (Optional[bool]): if True minus is included.
            Defaults to False.
        with_special_characters (Optional[bool]): if True special characters are included.
            Defaults to False.
        with_brackets (Optional[bool]): if True brackets are included.
            Defaults to False.
        format (Optional[str]): type of format in which data should be returned
            Defaults to 'yaml'. Available choices: yaml, json

    """
    simple_gen = generator.SimpleGenerator(length, with_lower,
                                           with_upper, with_numbers,
                                           with_space, with_underscore,
                                           with_minus,
                                           with_special_characters,
                                           with_brackets)

    click.echo(simple_gen.serialize(format))


@click.group()
def cli3():
    pass


@cli3.command()
@click.option("--file", default='model.yml', help="YAML file with model definition")
@click.option('--format', type=click.Choice(['json', 'yaml']), default=None)
def model(file, format):
    """Model bases generator.

    This one is using models defined in yaml files to generate data

    Args:
        file (str): YAML file with model definition
        format (Optional[str]): type of format in which data should be returned
            Defaults to 'yaml'. Available choices: yaml, json

    """
    models_gen = models.ModelBasedGenerator.load(file)
    click.echo(models_gen.serialize(format))


cli = click.CommandCollection(sources=[cli1, cli2, cli3])


if __name__ == "__main__":
    cli()
