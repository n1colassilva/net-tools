"""
Code pertaining to the CLI and related classes

Handles a base cli program that is made to be reliable and flexible, some would call it a framework
"""

# TODO later: finish the TODO's in the parser # this will be here for a while
# TODO Later: Reestructure parser so it isnt barely readable

from typing import Any, Callable, Literal
from user_interface import display_user_prompt
from utils.console_messages import console_msg


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
                self,
                short_name: str,
                long_name: str,
                arg_amount: int,
                arg_type: type[Any],
                help_str: str,
            ) -> None:
                self.short_name: str = short_name
                self.long_name: str = long_name
                self.arg_amount: int = arg_amount
                self.arg_type: type[Any] = arg_type
                self.help_str: str = help_str

        class Arg:
            def __init__(self, name: str, arg_type: type[Any], default: Any):
                self.name: str = name
                self.arg_type: type[Any] = arg_type
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
            argument = Cli.Command.Arg(name, arg_type, default)
            self.arg_data.append(argument)

        def set_flag(
            self,
            short_name: str,
            long_name: str,
            args_amount: int,
            arg_type: type[Any],
            help_str: str,
        ):
            """
            Stores flag data for the command.

            Args:
                    name         (tuple[str]):  One-letter flag (e.g., '-v') or long flag (e.g., '--verbose').
                    args_amount  (int):         Number of arguments the flag takes. 0 for no arguments.
                    arg_type     (type[Any]):   Expected type for the flag's argument. None if no arguments.
                    help_str     (str):         Description of the flag for user reference.

            Important Note: Flags with multiple arguments of different types are not
            supported.
                    - If this situation arises, consider refactoring your logic or
                    creating a separate function.
                    - Handling such complexity within flags leads to poor
                    maintainability and anti-patterns.
            """

            new_flag_data = Cli.Command.Flag(
                short_name, long_name, args_amount, arg_type, help_str
            )

            self.flag_data.append(new_flag_data)

    class FlagData:
        """
        Class for storing input flags with their arguments
        """

        def __init__(self, flag_type: "Cli.Command.Flag", flag_args: list[str] | None):
            self.flag_type: Cli.Command.Flag = flag_type
            self.list_args: list[str] | None = flag_args

        def _check_arg_type(self, arg: str):
            return True if isinstance(arg, self.flag_type.arg_type) else False

        def validate_all_types(self):
            """Checks the type of each flag argument"""

            if self.flag_type.arg_type[0] is None and self.list_args is None:
                return True

            if self.list_args is None:
                return False  # TODO communicate the error better

            for flag_arg in self.list_args:
                if not self._check_arg_type(flag_arg):
                    return False  # TODO communicate the error better
            return True

        def convert_into_valid_types(self) -> None | list[Any] | Literal[True]:
            """
            Converts flag arguments to their expected types, handling empty flags for booleans.

            Returns:
                A list of converted flag arguments (None for empty boolean flags),
                or None if type validation fails.
            """

            if self.flag_type.arg_amount == 0 and self.list_args is None:
                # Empty flag for a boolean type
                return True  # Return True for empty boolean flag

            if self.list_args is None:
                return None  # Missing argument for a non-boolean flag (error)

            converted_args: list[Any] = []
            target_type: type[Any] = self.flag_type.arg_type

            # Convert each flag argument to its expected type
            for flag_arg in self.list_args:
                try:
                    converted_args.append(target_type(flag_arg))
                except (ValueError, TypeError):
                    return None  # Type conversion error (communicate the error better)

            return converted_args

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
        print(f"registered {command}")
        self.commands.append(command)

    def run(self):
        """Prompts the user for input and executes the corresponding command."""

        while True:
            input_string: str = display_user_prompt(self.cli_name)

            # send this to the parser
            parsed_input = self.parser(input_string)
            if parsed_input is None:
                continue
            else:
                self.tasker(parsed_input[0], parsed_input[1], parsed_input[2])

    def parser(
        self, user_input: str
    ) -> None | tuple[Command, list[FlagData], list[str]]:
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
                console_msg("error", "Uknown command")
                return

        if not isinstance(command_data, Cli.Command):  # Checking if we actually got it
            console_msg(
                "error", f"Invalid command: {input_command} is not a valid command"
            )
            console_msg("info", "Type `help` to learn what commands are available")
            return

        # If your code editor supports folding, do it to flag_data, it's only used for output
        flag_list: list[Cli.FlagData] = []
        arg_list: list[str] = []
        # Separate arguments and flags
        # we can get flags first since their syntax is more obvious
        for h, arg in enumerate(args):
            if arg.startswith("-") is True:  # who the hell wrote "is not false"
                args.pop(h)  # removing the flag from the string
                for i, flag in enumerate(command_data.flag_data):
                    if arg == flag.short_name or arg == flag.long_name:
                        if flag.arg_amount != 0:
                            grabbed_flag_args: list[str] = []
                            for j in range(flag.arg_amount):
                                grabbed_flag_args[j] = args.pop(
                                    j + i
                                )  # Storing and removing flag arguments from args
                            # Actually putting it into the flag_data class
                            flag_list.append(self.FlagData(flag, grabbed_flag_args))
                            # This code is bad and ugly but i dont have time to fix
                            # Hope this doesn't come back to bite me in the rear
                            # ^ :clueless:
            else:
                arg_list.append(args[h])

        return command_data, flag_list, arg_list

    def tasker(self, command: Command, flags: list[FlagData], args: list[str]):
        """Runs the appropriate command with type converted flags and args"""

        # Check and convert flag types into validated_flags
        validated_flags: list[Any] = []
        try:
            for flag in flags:
                validated_flags.append(flag.convert_into_valid_types())
        except ValueError:
            console_msg("error", f"Invalid flag type")
            console_msg(
                "hint",
                f"Check proper command arg type order using `help {command.name}`",
            )

        # Processing Args into validated_args
        validated_args: list[Any] = []
        for i, arg in enumerate(args):
            try:
                validated_args.append(command.arg_data[i].arg_type[0](arg))
            except ValueError:
                console_msg("error", "Invalid arg type, ")
                console_msg(
                    "info",
                    f"{command.arg_data[i].name} is supposed to be a {command.arg_data[i].arg_type}",
                )
        # Type converting args # We just convert, not our problem
        # Type checking args   # Check previous
