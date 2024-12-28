# -*- coding: utf-8 -*-

"""
Internationalization support
"""

import argparse
import gettext

from pathlib import Path
from typing import Callable


MODULES_DIRECTORY = Path(__file__).resolve().parent
LOCALE_DIRECTORY = MODULES_DIRECTORY / "locale"


def translate_argparse() -> None:
    """Helper function: translate argparse
    (adapted from <https://github.com/s-ball/i18nparse>)
    """
    translation = gettext.translation(
        "argparse",
        localedir=LOCALE_DIRECTORY,
        fallback=True,
    )
    argparse._ = translation.gettext  # type: ignore
    argparse.ngettext = translation.ngettext  # type: ignore


def get_gettext() -> Callable[[str], str]:
    """Provide the gettext function for this package"""
    return gettext.translation(
        "ipsh", localedir=LOCALE_DIRECTORY, fallback=True
    ).gettext
