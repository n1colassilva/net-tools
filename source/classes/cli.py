"""
Code pertaining to the CLI and related classes

Handles a base cli program that is made to be reliable and flexible, some would call it a framework
"""

# Note to self: move into using objects, named tuples didnt work
from os import name
from typing import Any, Callable, Union
from user_interface import display_user_prompt


class Cli:

    class Command:
        """
        Class to represent a command with its associated data.

        You need to:
        - Register the function to execute for the command.
        - Register any arguments required by the command.
        - Register any flags that can be used with the command.

        The `help_str` provides a description of the command for user reference.

        Why are flags and arguments separate?
        - Arguments are mandatory inputs for the command.
        - Flags are optional and may or may not take additional arguments themselves.
        """

        class Flag:
            def __init__(
                self, name: str, arg_amount: int, arg_type: type[Any], help_str: str
            ) -> None:
                self.name: str = name
                self.arg_amount: int = arg_amount
                self.arg_type: type[Any] = arg_type
                self.help_str: str = help_str

        class Arg:
            def __init__(self, name: str, type: type[Any], default: Any):
                self.name: str = name
                self.type: type[Any] = type
                self.default: Any = default

        def __init__(self) -> None:
            """
            Initiates the command variables:


            """
            self.name: str = ""  # Set an initial empty name
            self.function: Callable[..., Any]  # Function to execute
            self.help_str: str = ""  # Help description
            self.arg_data: list[Cli.Command.Arg] = []
            self.flag_data: list[Cli.Command.Flag] = []

        def set_function(self, name: str, function: Callable[..., Any], help_str: str):
            """
            Registers the function to be executed for this command.

            Args:
                    name     (str):                 Name of the command, ideally one or two words.
                    function (Callable[..., Any]):  The function to execute.
                    help_str (str):                 Description for user reference.
            """
            self.name = name
            self.function = function
            self.help_str = help_str

        def set_argument(self, name: str, arg_type: type[Any], default: Any):
            """
            Adds an argument to the command's argument list.

            Args:
                    name     (str):         Name of the argument.
                    arg_type (type[Any]):   Expected data type for the argument.
                    default  (Any):         Default value for the argument (optional).
            """
            argument = {"name": name, "type": arg_type, "default": default}
            self.arg_data.append(argument)

        def set_flag(
            self, name: tuple[str], args_amount: int, arg_type: type[Any], help_str: str
        ):
            """
            Stores flag data for the command.

            Args:
                    name         (tuple[str]):  One-letter flag (e.g., '-v') or long
                                                flag (e.g., '--verbose').
                    args_amount  (int):         Number of arguments the flag takes
                                                (0 for no arguments).
                    arg_type     (type[Any]):   Expected type for the flag's argument
                                                (None if no arguments).
                    help_str     (str):         Description of the flag for user reference.

            Important Note: Flags with multiple arguments of different types are not supported.
                    - If this situation arises, consider refactoring your logic or creating a
                    separate function.
                    - Handling such complexity within flags leads to poor maintainability and
                    anti-patterns.
            """

            new_flag_data = Cli.Command.Flag(name, args_amount, arg_type, help_str)

            self.flag_data.append(new_flag_data)

    def __init__(self, _cli_name: str):
        """
        Initiates the CLI instance.

        Args:
            _cli_name (str): The name that will be displayed in the user promp.
        """
        self.commands: list[Cli.Command] = []
        self.cli_name: str = _cli_name if _cli_name else ""

    def register_command(self, command: Command) -> None:
        """Saves your command into the CLI (command created by Command's functions)"""

        self.commands.append(command)

    def run(self):
        """Prompts the user for input and executes the corresponding command."""

        while True:
            input_string: str = display_user_prompt(self.cli_name)

            # send this to the parser
            self.parser(input_string)

    def parser(self, user_input: str):
        args = user_input.split(" ")

        # Get main command
        input_command = args.pop()  # First word always command

        # Try to find the relevant command data
        command_data: Cli.Command | None = None
        for cmd in self.commands:
            if cmd.name == input_command:
                command_data = cmd
                break
            else:
                ...
                return
                # TODO: BIG ERROR

        if not isinstance(command_data, Cli.Command):  # Checking if we actually got it
            return

        # Separate arguments and flags
        # we can get flags first since their syntax is more obvious
        for arg in args:
            if arg.startswith("-") is not False:
                for flag in command_data.flag_data:
                    # if arg == flag
                    ...  # flag
            else:
                ...  # Not flag

        # Get command arguments
        # Get command flags
        # Get flag's arguments (if it applies)
