# -*- coding: utf-8 -*-

"""
ipsh main cli script
"""

import argparse
import logging
import sys

from . import __version__
from . import interpreters
from . import i18n


_ = i18n.get_gettext()

COMMAND_DEMO = "demo"
COMMAND_SHOWKEYS = "showkeys"


def get_arguments(*args: str, test_context: bool = False) -> argparse.Namespace:
    """Get commandline arguments"""
    i18n.translate_argparse()
    main_parser = argparse.ArgumentParser(
        prog="ipsh", description=_("interactive pseudo shell command line interface")
    )
    main_parser.set_defaults(loglevel=logging.INFO)
    main_parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        help=_("debug mode (loglevel DEBUG)"),
    )
    main_parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help=_("print version and exit"),
    )
    if not test_context or not args:
        args_to_parse: list[str] | None = None
    else:
        args_to_parse = list(args)
    #
    return main_parser.parse_args(args=args_to_parse)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger with loglevel _level_"""
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    root_logger = logging.getLogger()
    stream_handlers = [
        handler
        for handler in root_logger.handlers
        if isinstance(handler, logging.StreamHandler)
    ]
    if stream_handlers:
        current_handler = stream_handlers[0]
    else:
        current_handler = logging.StreamHandler()
        root_logger.addHandler(current_handler)
    #
    current_handler.setFormatter(formatter)
    current_handler.setLevel(level)
    root_logger.setLevel(level)


def run(*args: str, test_context: bool = False) -> int:
    """Run the main program"""
    arguments = get_arguments(*args, test_context=test_context)
    configure_logging(level=arguments.loglevel)
    interpreter = interpreters.BaseArgumentsInterpreter()
    description = _("a PseudoShell demo with an argparse based interpreter")
    logging.info(_("Running %s"), description)
    interpreter.cmdloop()
    return 0


def app():
    """app function"""
    sys.exit(run())
