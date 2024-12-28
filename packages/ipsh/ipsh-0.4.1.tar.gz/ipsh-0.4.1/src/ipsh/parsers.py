# -*- coding: utf-8 -*-

"""
Argument parsers
"""

import argparse
import dataclasses

import sys

from typing import Any, Self


class FrozenInstanceError(Exception):
    """Raised if a frozen intance was tried to change"""


class ParserExit(Exception):
    """Raised if a parser exits"""


class PatchedArgparseError(Exception):
    """Raised if the PatchedArgumentParser encountered ana error situation"""

    def __init__(self, message: str) -> None:
        """Initialization argument: _message_ – the error message"""
        self.message = message

    def __str__(self) -> str:
        """String value (the message itself)"""
        return self.message


@dataclasses.dataclass(frozen=True)
class ArgumentDefinition:
    """Definition of a single argument"""

    args: tuple[str, ...]
    kwargs: dict[str, Any]

    @classmethod
    def as_added(cls, *args, **kwargs) -> Self:
        r"""Return an instance made from the same arguments as an
        argument in an argumant parser would have been made through the
        .add\_argument(\*args, \*\*kwargs) method
        """
        return cls(args=args, kwargs=kwargs)


class Prototype:
    """Prototype containing all information required
    to create an argument parser, except for the name and description
    """

    def __init__(
        self,
        *argdefs: ArgumentDefinition,
        add_help: bool = True,
        exit_on_error: bool = False,
        do_freeze: bool = True,
    ) -> None:
        r"""Initialization arguments:

        -   _argdefs_: any number of [ArgumentDefinition] instances
        -   _add\_help_: add a -h / --help option
        -   _exit\_on\_error_: exit on errors
        -   _do\_freeze_: : freeze the instance after initialization
        """
        self.__frozen = False
        self.add_help = add_help
        self.exit_on_error = exit_on_error
        self.__protoparser = argparse.ArgumentParser(
            "prototype", add_help=add_help, exit_on_error=False
        )
        self.argument_definitions: list[ArgumentDefinition] = []
        for single_argdef in argdefs:
            self.add_argument_definition(single_argdef)
        #
        if do_freeze:
            self.freeze()
        #

    @property
    def is_frozen(self) -> bool:
        """Indicates if the instance is frozen or not"""
        return self.__frozen

    def freeze(self) -> None:
        """Freeze the instance"""
        self.__frozen = True

    def add_argument_definition(self, argdef: ArgumentDefinition) -> None:
        """Add the _argdef_ [ArgumentDefinition] instance
        after lazily checking it for correctness through the
        internally stored dummy argument parser
        """
        if self.is_frozen:
            raise FrozenInstanceError
        #
        self.__protoparser.add_argument(*argdef.args, **argdef.kwargs)
        self.argument_definitions.append(argdef)

    def add_argument(self, *args, **kwargs) -> None:
        r"""Create a new [ArgumentDefinition] instance using _aegs_ and _kwargs_,
        then add it through the [.add_argument_definition() method]
        """
        self.add_argument_definition(ArgumentDefinition(args=args, kwargs=kwargs))


class ModifiedArgumentParser(argparse.ArgumentParser):
    r"""[argparse.ArgumentParser] instances in Python 3.11 and before
    exit with an error in certain cases in spite of initialization with
    `exit_on_error=False`, and printing help also exists the Python script
    in all observed versions.

    This class modifies the behavior of the .error() and .exit() methods
    to never actually exit the Python script.
    """

    def exit(self, status=0, message=None):
        """Do not exit the script directly from the agrument parser,
        just write _message_ to sys.stderr. The status argument is not used
        but merely provided for matching the parent class method.
        """
        if message:
            sys.stderr.write(message)
        #
        del status
        raise ParserExit

    def error(self, message):
        """Raises a **[PatchedArgparseError]** with _message_ unconditionally"""
        raise PatchedArgparseError(message)

    @classmethod
    def from_prototype(cls, name: str, description: str, prototype: Prototype) -> Self:
        """Return a new instance from _name_, _description_, and _prototype_"""
        new_parser = cls(
            name,
            description=description,
            add_help=prototype.add_help,
            exit_on_error=prototype.exit_on_error,
        )
        for argdef in prototype.argument_definitions:
            new_parser.add_argument(*argdef.args, **argdef.kwargs)
        #
        return new_parser
