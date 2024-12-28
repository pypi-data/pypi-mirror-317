# -*- coding: utf-8 -*-

"""
test the ipsh.interpreters module
"""

import io

from unittest import TestCase

from unittest.mock import patch

from ipsh import interpreters


SYS_STDOUT = "sys.stdout"


class BaseArgumentsInterpreter(TestCase):
    """Test the BaseArgumentsInterpreter"""

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_help_command(self, mock_stdout) -> None:
        """test the help command"""
        abi = interpreters.BaseArgumentsInterpreter()
        with self.subTest("no exit"):
            self.assertFalse(abi.onecmd("help"))
        #
        ruler = abi.ruler * len(abi.doc_header)
        commands = sorted(abi.argument_parsers)
        cmds_line = "  ".join(commands)
        with self.subTest("help output"):
            self.assertIn(
                f"{abi.doc_header}\n{ruler}\n{cmds_line}", mock_stdout.getvalue()
            )
        #

    def test_history_command(self) -> None:
        """test history command"""
        abi = interpreters.BaseArgumentsInterpreter()
        command_1 = "history -h"
        command_2 = "history 1"
        command_3 = "history"
        with self.subTest("command help"):
            with patch(SYS_STDOUT, new_callable=io.StringIO) as mock_stdout:
                abi.precmd(command_1)
                abi.onecmd(command_1)
                self.assertIn("usage: history [-h] [number]", mock_stdout.getvalue())
            #
        #
        with self.subTest("command execution", scope="last entry only"):
            with patch(SYS_STDOUT, new_callable=io.StringIO) as mock_stdout:
                abi.precmd(command_2)
                abi.onecmd(command_2)
                self.assertIn(f"  [2]  {command_2}", mock_stdout.getvalue())
            #
        #
        with self.subTest("command execution", scope="all entries"):
            with patch(SYS_STDOUT, new_callable=io.StringIO) as mock_stdout:
                abi.precmd(command_3)
                abi.onecmd(command_3)
                self.assertIn(
                    "\n".join(
                        f"  [{idx}]  {command}"
                        for idx, command in (
                            (1, command_1),
                            (2, command_2),
                            (3, command_3),
                        )
                    ),
                    mock_stdout.getvalue(),
                )
            #
        #

    def test_exit_command(self) -> None:
        """test the exit command"""
        abi = interpreters.BaseArgumentsInterpreter()
        self.assertTrue(abi.onecmd("exit"))
