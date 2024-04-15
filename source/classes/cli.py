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
            self.runner_function: Callable[
                [Cli.CommandData], None
            ]  # Function to execute
            self.help_str: str = ""  # Help description
            self.arg_data: list[Cli.Command.Arg] = []
            self.flag_data: list[Cli.Command.Flag] = []

        def set_function(
            self,
            name: str,
            function: Callable[["Cli.CommandData"], None],
            help_str: str,
        ):
            """
            Registers the function to be executed for this command.

            Args:
                    name     (str):                                 Name of the command,ideally one or two words.
                    function (Callable[[Cli.CommandData], None]):   The function to execute.
                    help_str (str):                                 Description for user reference.
            """
            self.name = name
            self.runner_function = function
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
            self.args_list: list[str] | None = flag_args

        def _check_arg_type(self, arg: str):
            return True if isinstance(arg, self.flag_type.arg_type) else False

        def validate_all_types(self):
            """Checks the type of each flag argument"""

            if self.flag_type.arg_type[0] is None and self.args_list is None:
                return True

            if self.args_list is None:
                return False  # TODO communicate the error better

            for flag_arg in self.args_list:
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

            if self.flag_type.arg_amount == 0 and self.args_list is None:
                # Empty flag for a boolean type
                return True  # Return True for empty boolean flag

            if self.args_list is None:
                return None  # Missing argument for a non-boolean flag (error)

            converted_args: list[Any] = []
            target_type: type[Any] = self.flag_type.arg_type

            # Convert each flag argument to its expected type
            for flag_arg in self.args_list:
                try:
                    converted_args.append(target_type(flag_arg))
                except (ValueError, TypeError):
                    return None  # Type conversion error (communicate the error better)

            return converted_args

    class CommandData:
        def __init__(self) -> None:
            self.command: Cli.Command
            self.flags: list[Cli.FlagData]
            self.args: list[Any]

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
            parsed_input: Cli.CommandData | None = self.parser(input_string)
            if parsed_input is None:
                continue
            else:
                self.tasker(parsed_input)

    def parser(self, user_input: str) -> CommandData | None:
        """
        Separates the user input into its constituent parts and returns a CommandData object containing, well, the command data (as in the command type, the args and flags and the flag args)

        Args:
            user_input (str): What the user wrote down.

        Returns:
            CommandData | None: The parsed input
        """

        # Initializing our returns

        return_command = Cli.CommandData()

        # Before we even start, check if we have commands
        if self.commands == []:
            console_msg("error", "No commands registered, aborting")
            return None

        input_list = user_input.split(" ")

        input_command = input_list.pop(0)

        command: Cli.Command | None
        # Let's find the command
        command = None
        for registered_command in self.commands:
            if input_command == registered_command.name:
                command = registered_command
                break
        # Checking command exists
        if command is None:
            return None

        # Set the command
        return_command.command = command
        # Might as well initialize everything
        return_command.flags = []
        return_command.args = []

        # Scary: we are going to go through all the other stuff to find what we want and need
        for i, input in enumerate(input_list):

            # Detecting flags
            if input.startswith("-"):

                for flag in command.flag_data:
                    if flag.short_name == input or flag.long_name == input:
                        # Found a match, grabbing args if any
                        flag_args: list[str] = []
                        if flag.arg_amount > 0:
                            # There are args, let's grab them
                            for flag_arg in range(flag.arg_amount):
                                flag_args.append(input_list.pop(i + flag_arg))

                        return_command.flags.append(Cli.FlagData(flag, flag_args))

                        # We are done here, prepare to get out
                        # input_list.pop(i) # Not sure this will be necessary
                        break
                    else:
                        console_msg("error", "Invalid flag")
                        return None
            else:  # It's an argument
                return_command.args.append(input)

        return return_command

    def tasker(self, command_data: "Cli.CommandData") -> None:
        """
        Recieves a CommandData object and runs the command's registered runner for yet another round of parsing

        Args:
            command_data (Cli.CommandData): the CommandData created by the Cli.parser function.
        """

        command_data.command.runner_function(command_data)
