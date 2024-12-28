# -*- coding: utf-8 -*-

"""
Interpreter definitions
"""

import argparse
import cmd
import logging
import shlex

from . import history
from . import i18n
from . import parsers


_ = i18n.get_gettext()

CMD_EXIT = "exit"
CMD_HELP = "help"
CMD_HISTORY = "history"

MSG_HISTORY = _("History:")

PROTOTYPE_HELP = parsers.Prototype(
    parsers.ArgumentDefinition.as_added(
        "topic",
        nargs="?",
        help=("the help topic (one of the available commands)"),
    ),
)
PROTOTYPE_HISTORY = parsers.Prototype(
    parsers.ArgumentDefinition.as_added(
        "number",
        nargs="?",
        help=_("the number of history entries to show (all entries by default)"),
        type=int,
        default=-1,
    ),
)
PROTOTYPE_WITH_ARBITRARY_POSITIONAL_ARGS = parsers.Prototype(
    parsers.ArgumentDefinition.as_added(
        "positional", nargs="*", help=_("arbitrary positional arguments")
    ),
)
PROTOTYPE_WITHOUT_ARGS = parsers.Prototype()


class InterpreterExit(Exception):
    """Raised on Interpreter exit"""


class NoExecutionAllowed(Exception):
    """Raised and handled internally to control behavior
    in case of argument errors or help display
    """


class BaseArgumentsInterpreter(cmd.Cmd):
    """Interpreter base class doing arguments parsing
    for each defined command
    """

    default_prototype = PROTOTYPE_WITHOUT_ARGS
    prompt = " → "

    def __init__(
        self,
        completekey="tab",
        stdin=None,
        stdout=None,
        history_buffer: history.History = history.History(),
    ) -> None:
        """Initialize the interpreter"""
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        i18n.translate_argparse()
        self.__history = history_buffer
        self.__parsers: dict[str, parsers.ModifiedArgumentParser] = {}
        self.add_parser(CMD_EXIT, PROTOTYPE_WITHOUT_ARGS)
        self.add_parser(CMD_HELP, PROTOTYPE_HELP)
        self.add_parser(CMD_HISTORY, PROTOTYPE_HISTORY)
        self.prompt = self.__class__.prompt

    @property
    def argument_parsers(self) -> dict[str, parsers.ModifiedArgumentParser]:
        """A shallow copy of the internal parsers mapping"""
        return self.__parsers.copy()

    def add_parser(
        self, name: str, prototype: parsers.Prototype = default_prototype
    ) -> None:
        """Add a parser"""
        if name not in self.__parsers:
            try:
                handler_method = getattr(self, f"do_{name}")
            except AttributeError:
                return
            #
            self.__parsers[name] = parsers.ModifiedArgumentParser.from_prototype(
                name, handler_method.__func__.__doc__, prototype
            )
        #

    def parse_arguments(self, command_name: str, arg: str) -> argparse.Namespace:
        """parse the provided _arg_ and return a **ParseResult** instance"""
        parts = shlex.split(arg)
        try:
            namespace = self.__parsers[command_name].parse_args(parts)
        except (
            KeyError,
            parsers.PatchedArgparseError,
            argparse.ArgumentError,
        ) as error:
            logging.error(str(error))
            raise NoExecutionAllowed from error
        except parsers.ParserExit as parser_exit:
            raise NoExecutionAllowed from parser_exit
        #
        return namespace

    def cmdloop(self, intro=None) -> None:
        """Wrap the super class’ cmdloop method to catch
        the InterpreterExit exception
        """
        try:
            return super().cmdloop(intro)
        except InterpreterExit:
            print()
            return None
        #

    def emptyline(self):
        """Override the default behavior:
        do nothing instead of re-executing the last command
        """
        return False

    def precmd(self, line):
        """put the line into accessible history,
        and ensure a matching parser exists
        """
        if line == "EOF":
            raise InterpreterExit
        #
        if not line.strip():
            return line
        #
        self.__history.add(line)
        parts = shlex.split(line)
        if not parts:
            return line
        #
        command_name = parts[0]
        if command_name == "?":
            command_name = CMD_HELP
        #
        self.add_parser(command_name)
        return line

    def do_exit(self, arg):
        """Exit the interpreter"""
        try:
            self.parse_arguments(CMD_EXIT, arg)
        except NoExecutionAllowed:
            return False
        #
        return True

    def do_help(self, arg):
        """List available commands with "help",
        or detailed help with "help topic",
        where "topic" is the command name to display help for.
        """
        try:
            self.parse_arguments(CMD_HELP, arg)
        except NoExecutionAllowed:
            return
        #
        super().do_help(arg)

    def do_history(self, arg):
        """List history entries"""
        try:
            arguments = self.parse_arguments(CMD_HISTORY, arg)
        except NoExecutionAllowed:
            return
        #
        print(MSG_HISTORY)
        for idx, line in self.__history.iter_range(start=-arguments.number):
            print(f"  [{idx}]  {line}")
        #
