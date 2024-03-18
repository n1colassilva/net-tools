from typing import Any, Callable
from user_interface import display_user_prompt
import argparse


class CLI:
    """Base class for a borrowable command-line interface."""

    class Command:

        class Arg:
            def __init__(
                self,
                short_name: str,
                long_name: str,
                type: type,
                default_value: Any,
                help: str,
            ):
                """
                Stores an argument

                Args:
                    short_name       (str):     Short version of the name (ex: `-v`)
                    long_name        (str):     Long version of the name (ex: `--Version`)
                    type             (type):    Type of the argument (ex: `int`)
                    default_value    (Any):     Default value (`2`)
                    help             (str):     What should be printed out when the help tag is added (-h,--help), should cover what the argument does
                """
                self.short_name: str = short_name
                self.long_name: str = long_name
                self.type: type = type
                self.default_value: Any = default_value
                self.help: str = help

        def __init__(self) -> None:
            self.function: Callable[[], None]
            self.name: str
            # self.args

    def __init__(self, _cli_name: str):
        """
        Initiates the CLI instance.

        Args:
            _cli_name (str): The name that will be displayed in the user promp.
        """
        self.commands: dict[str, Callable[[], None]] = {}

        self.cli_name: str = _cli_name if _cli_name else ""

    def register_command(self, name: str, function: Callable[[], None]) -> None:
        """
        Registers a new command with the CLI.

        Args:
            name (str): The name of the command.
            function (Callable[[], None]): The function to be executed for the command.

        Returns:
            None
        """

        self.commands[name] = function

    def run(self):
        """
        Prompts the user for input and executes the corresponding command.
        """

        while True:
            input_string = display_user_prompt(self.cli_name)

            arguments = input_string.split(" ")
            command = arguments.pop()

            # No need for `and not arguments` since no command -> no arguments
            if not command:
                continue

            if command in self.commands:
                self.commands[command]()
            else:
                print(f"Error: Unknown command '{command}'.")
