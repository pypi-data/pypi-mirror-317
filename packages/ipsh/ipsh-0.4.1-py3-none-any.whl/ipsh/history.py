# -*- coding: utf-8 -*-

"""
Command history support
"""

from typing import Iterator

from . import i18n


_ = i18n.get_gettext()

HISTORY_PLACEHOLDER_EMPTY = _("(empty)")

MSG_NOT_AVAILABLE = _("Not available")
MSG_UNSPECIFIED = _("unspecified")


class HistoryError(Exception):
    """Error from a history instance"""

    def __init__(self, message: str = MSG_UNSPECIFIED) -> None:
        """Initialization argument: _message_ – the error message"""
        self.message = message

    def __str__(self) -> str:
        """String value (the message itself)"""
        return self.message


class History:
    """Command history storage
    with an internally stored, mutable position
    """

    def __init__(self) -> None:
        """Normally, the current position is
        after the last entry of the buffer
        """
        self.__entries: list[str] = [HISTORY_PLACEHOLDER_EMPTY]
        self.__position = len(self)

    def __len__(self):
        """Number of entries in the buffer"""
        return len(self.__entries)

    def __getitem__(self, pos: int):
        """Return the buffer entry at _pos_.
        Raises a HistoryError on unsupported values of _pos_.
        """
        if pos < 1:
            raise HistoryError(MSG_NOT_AVAILABLE)
        #
        if pos == len(self):
            return ""
        #
        try:
            found_entry = self.__entries[pos]
        except IndexError as error:
            raise HistoryError(MSG_NOT_AVAILABLE) from error
        #
        return found_entry

    @property
    def position(self) -> int:
        """The current position"""
        return self.__position

    def add(self, line: str):
        """Add _line_ to the buffer and set the position to thr buffer end"""
        self.__entries.append(line)
        self.__position = len(self)

    def get_relative(self, delta: int):
        """Get an entry from the relative buffer index _delta_.
        Might raise a HistoryError indirectly.
        """
        new_position = self.position + delta
        found_entry = self[new_position]  # raises the HistoryError if appropriate
        # If everything went fine and an entry was found,
        # adjust the position and return the found entry
        self.__position = new_position
        return found_entry

    def iter_range(self, start=1, end=-1) -> Iterator[tuple[int, str]]:
        """Return an iterator over (index, entry) tuples
        in the specified range between _start_ and _end_.
        """
        if end < 0:
            end = len(self) + end
        #
        if start < 0:
            start = len(self) + start
        #
        for idx in range(start, end + 1):
            try:
                yield idx, self[idx]
            except HistoryError:
                ...
            #
        #
