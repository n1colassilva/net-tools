"""
Contains functions for displaying the help command, there are 2 versions meant for 2 purposes:

- show_help prints about every registered command, doesn't explain its args or flags;

- command_help prints detailed info for each command, down to the arguments and flags
"""

from classes.cli import Cli
from utils.console_messages import console_msg


def show_help(cli: Cli, _command_data:Cli.CommandData):
    """Shows the help for all registered commands in the Cli."""

    print("Net-tools is a cli tool for simple network analisys\n")

    for command in cli.commands:
        print(command.help_str)


def command_help(cli: Cli, command_data:Cli.CommandData):
    """Shows the help for a specific command."""

    input_command = command_data.args[0]
    # Finding the command
    command = None  # We don't know what it is yet

    for cli_command in cli.commands:
        if cli_command.name == input_command:
            command = cli_command
            break

    if command == None:  # If we still don't know we bail
        console_msg("error", "Invalid or nonexistant command name.")
        return

    print(f"{command.name}\t{command.help_str}")

    for arg in command.arg_data:
        print(f"\t{arg.name} ({(arg.arg_type[0])})")

    for flag in command.flag_data:
        print(f"\t{flag.short_name}/{flag.long_name}\t{flag.help_str}")
        if flag.arg_amount > 0:
            print(f"\t\t takes {flag.arg_amount} of {flag.arg_type}")


# Command registration


def register_show_help(cli: Cli):
    """Registers the show help function."""

    command = Cli.Command()
    command.set_function(
        "help",
        show_help,
        "Shows all the available commands and what they do.",
    )
    # Not sure how everything will behave because this function doesn't take any arguments
    cli.register_command(command)


def register_command_help(cli: Cli):
    """Registers the command help function."""

    command = Cli.Command()
    command.set_function(
        "info", command_help, "Shows information on how a command works"
    )
    command.set_argument("command name", str, "")
    cli.register_command(command)

