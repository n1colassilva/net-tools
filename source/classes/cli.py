"""
Code pertaining to the CLI and related classes

Handles a base cli program that is made to be reliable and flexible, some would call it a framework
"""
# Note to self: last thing i was working on is figuring out the type tomfoolery
# Maybe move them into being public would solve the problem
# Look into a better way, maybe using an object so we dont have to deal with those hoops
# Maybe there is a way to make pylance not question our choice in having an object with no methods
from typing import Any, Callable, Literal
from user_interface import display_user_prompt


class CLI:
    """Base class for a borrowable command-line interface."""

    class COMMAND:
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
            self.arg_data: list[dict[CLI.COMMAND.argument_data_indexes, str | type[Any] | Any]]
            self.flag_data: dict[CLI.COMMAND.flag_data_indexes, Any]

        def set_function(self, name: str, function: Callable[..., Any], help_str: str):
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

        argument_data_indexes=Literal[
            "name",
            "type",
            "default"
        ]

        def set_argument(self, name: str, arg_type: type[Any], default: Any):
            """
            Adds an argument to the argument list

            Args:
                name     (str):         Name of the argument
                arg_type (type[Any]):   Type the argument expects
                default  (Any):         Default value
            """
            argument: dict[CLI.COMMAND.argument_data_indexes, str | type[Any] | Any] = {
                "name": name,
                "type": arg_type,
                "default": default,
            }
            self.arg_data.append(argument)

        # Creating a type so we get type hints
        flag_data_indexes = Literal[
            "name",
            "amount",
            "type",
            "help"
        ]

        def set_flag(
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
            self.flag_data: dict[CLI.COMMAND.flag_data_indexes, Any] = {
                "name": name,
                "amount": args_amount,
                "type": args_type,
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
        self.commands: list[CLI.COMMAND] = []
        self.cli_name: str = _cli_name if _cli_name else ""

    def register_command(self, command: COMMAND) -> None:
        """
        Saves your command into the CLI (command created by COMMAND's functions)

        Args:
            command (COMMAND): _description_
        """

        self.commands.append(command)

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

    def parser(self, user_input: str):
        args = user_input.split(" ")

        # Get main command
        input_command = args.pop()  # First word always command

        # Try to find the relevant command data
        command_data: CLI.COMMAND
        for cmd in self.commands:
            if cmd.name == input_command:
                command_data = cmd
                break
            else:
                ...
                # TODO BIG ERROR

        # Separate arguments and flags
        # we can get flags first since their syntax is more obvious
        for arg in args:

            if arg.startswith("-"):
                for flag in command_data.flag_data:
                    if arg == 
                ...  # flag
            else:
                ...  # Not flag

        # Get command arguments
        # Get command flags
        # Get flag's arguments (if it applies)
