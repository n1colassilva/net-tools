"""
Code pertaining to the CLI and related classes

Handles a base cli program that is made to be reliable and flexible, some would call it a framework
"""

from typing import Any, Callable
from user_interface import display_user_prompt


class CLI:
    """Base class for a borrowable command-line interface."""

    class Command:
        """
        Class to create a command with it's related data

        You do need to:
        1. Register the function
        2. Register its arguments
        3. Register its flags

        The `help_str`s will be seen by the user when they ask for help

        Why are flags and arguments separate?
        - Arguments are obligatory in nature
        - Flags are optional, some may even take arguments of their own
        """

        def __init__(self) -> None:
            self.name: str
            # Callable takes any amount and type of arguments, returns Any
            self.function: Callable[..., Any]
            self.help_str: str
            self.arg_data: list[dict[str, str | type[Any] | Any]]
            self.flag_data: dict[str, Any]

        def register_function(
            self, name: str, function: Callable[..., Any], help_str: str
        ):
            """
            Registers the function proper

            Args:
                name     (str):                 Name of the function, keep it to one word around
                                                5-4 charachters
                function (Callable[..., Any]):  The actual function we are working with
                help_str (str):                 String containing help info

            Example:
                >>> kill_child_cli = Command()
                >>> kill_child_cli.register_function("kchild", kill_child, "kills a child")
            """
            self.name = name
            self.function = function
            self.help_str = help_str

        def register_argument(self, name: str, arg_type: type[Any], default: Any):
            """
            Adds an argument to the argument list

            Args:
                name     (str):         Name of the argument
                arg_type (type[Any]):   Type the argument expects
                default  (Any):         Default value
            """
            argument: dict[str, str | type[Any] | Any] = {
                "name": name,
                "type": arg_type,
                "default": default,
            }
            self.arg_data.append(argument)

        def register_flag(
            self,
            name: tuple[str],
            args_amount: int,
            args_type: type[Any],
            help_str: str,
        ):
            """
            Stores an argument

            Args:
                name             (tuple[str]):  Name of the flag (ex: `-v,--version`)
                help             (str):         What should be printed out when the
                help tag `-h` or `--help` is added, should cover what the argument does
            """
            self.flag_data: dict[str, Any] = {
                "name": name,
                "args_amount": args_amount,
                "args_type": args_type,
                "help": help_str,
                # "arg_types": arg_types,
                # If you get to the point where a flag gets multiple arguments of different types
                # You messed up big time!
                # refactor stuff, break it up of make that thing it's own function.
                # Even if i had the patience to handle that, it would take too much effort
                # and complexity, and in antipattern terms it's either blatantly bad or smells bad
            }

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
