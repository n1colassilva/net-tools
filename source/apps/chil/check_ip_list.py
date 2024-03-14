import ipaddress
import os
from termcolor import colored as clr
from utils.input_parser import input_parser

from ip_list import build_file_path, load_toml, add_entry
from utils.toml_print import toml_data_print as tprint
from utils.manyprint.mprint import multi_print as printm
from utils.console_messages import console_msg
from user_interface import display_user_prompt as prompt


class ChilTerm:

    def __init__(self):
        self.file_name: str = ""
        self.APP_NAME = f"{clr('chil 󰻽','white','on_blue',['bold'])}"
        # self.APP_NAME = f"{clr('chil 󰻽','white','on_blue',['bold'])}"
        self.display_name = self.APP_NAME

    def run(self):
        """Main terminal loop"""

        # Show splash screen
        self._splash()

        keep_running = True

        while keep_running:

            if self.file_name != "":
                self.display_name = (
                    self.APP_NAME + " 󰁔 " + "" + clr(self.file_name, attrs=["bold"])
                )

            user_input = prompt(self.display_name)
            command, arguments = input_parser(user_input)

            match command:
                case "select":
                    self.select_file(arguments[0])
                case "view":
                    self.display_file()
                case "insert":
                    self.insert()  # A writing/fanfic joke goes here.
                case "remove":
                    self.remove()
                case "create":
                    self.create(arguments[0])
                case "drop":
                    ...
                case _:
                    ...

    def _splash(self) -> None:
        """Prints chil's own splash screen"""
        printm(
            "'chil󰻽': Check IP List",
            "App for managing TOML files containig an ip list",
            "",
            "MIT license",
            "󰗦 Nícolas 2024",
            "",
            f"Type {clr('`help`','green' )} to see available commands\n",
        )

    def select_file(self, file_name: str) -> None:
        """Tries to find the toml and sets it as file_name"""
        data = load_toml(file_name)
        if data is None:
            console_msg("hint", "Use 'show-dir' to see all existant files")
        else:
            self.file_name = file_name

    def display_file(self) -> None:
        """Shows a file's data"""
        data: dict[str, dict[str, str]] | None = load_toml(self.file_name)

        if data is None:
            console_msg("error", "Empty file.")
            return

        printm(
            f"{clr(' ' + self.file_name,'cyan')}" "",
            "----------",
        )
        tprint(data)
        printm(
            "----------",
            "",
        )

    def insert(self) -> None:
        """
        Inserts and manages user input, collecting data into a dictionary.

        This function prompts the user for input repeatedly until the user enters
        "done". It parses the input using the `input_parser` function and takes action
        based on the provided command and arguments.

        Supported commands:

        * **done:** Exits the input loop.
        * **ip**: Takes an IP address as an argument and stores it in the dictionary
            with the key "ip". Validates the IP address using the `ipaddress` module and
            provides error messages for invalid input.
        * **name**: Takes a name as an argument and stores it in the dictionary
            with the key "name".
        * **description**: Takes a description as an argument and stores it in the
            dictionary with the key "description". Joins multiple words using
            " " as the separator.
        * **custom**: Takes a custom key and value as arguments and stores them in the
            dictionary with the provided key.
        * **write**: Takes a file path as an argument and uses the `build_file_path`
            function to construct the complete path. Then, calls the `add_entry`
            function to write the collected data (dictionary) to the specified file.
            Sets the `command` to "none" to prevent further input after writing.
        * **help**: Not implemented yet, but should display instructions on how to use
            the program.

        For any other unknown command, the function displays an error message and
        provides a hint to use "help" for further information.

        Args:
            self: An instance of the class containing this function.

        Returns:
            None. The function updates the internal state of the class and potentially
            writes data to a file, but doesn't return any value.
        """

        self.display_name = (
            self.APP_NAME
            + " 󰁔 "
            + clr("󰏪", "green")
            + " "
            + clr("" + self.file_name, "black", "on_white")
        )

        usr_dict: dict[str, str] = {}

        command: str = ""
        while command != "done":
            usr_input = prompt(self.display_name)

            command, args = input_parser(usr_input)

            match command.lower():
                case "done":
                    # here we break because the while will handle it
                    break
                case "ip":
                    # Checking for valid ip adress
                    try:
                        ipaddress.ip_address(args[0])
                    except ValueError:
                        console_msg("error", "Invalid ip adress")
                    finally:
                        usr_dict["ip"] = args[0]
                case "name":
                    usr_dict["name"] = args[1]
                case "description":
                    usr_dict["description"] = " ".join(args)
                case "custom":
                    usr_dict[args[0]] = args[1]
                case "write":
                    add_entry(args[1], usr_dict)
                    command = "none"  # A little hacky but will get the job done
                case _:
                    console_msg("error", "Invalid input.")
                    console_msg("hint", "Use 'help' to learn more")

    def remove(self) -> None:
        """Stars its own little cli to remove keys from the already picked file"""

        self.display_name = (
            self.APP_NAME
            + " 󰁔 "
            + clr("", "green")
            + " "
            + clr("" + self.file_name, "black", "on_white")
        )

        data: dict[str, dict[str, str]] | None = load_toml(self.file_name)

        if data is None:
            console_msg("error", "Invalid file.")
            return

        command: str = ""
        while command != "done":
            usr_input = prompt(self.display_name)

            command, args = input_parser(usr_input)

            match command.lower():
                case "done":
                    return
                case "remove":
                    try:
                        del data[args[0]]
                        console_msg("success", f"Removed key '{args[0]}'")
                    except KeyError:
                        console_msg("error", f"Key '{args[0]}' not found in dictionary")
                case "clear":
                    data.clear()
                    console_msg("success", "Dictionary cleared")
                case _:
                    console_msg("error", "Invalid input.")
                    console_msg(
                        "hint", "Use 'help' to learn more about remove functionality"
                    )

    def create(self, file_name: str) -> None:
        """Creates a new file, warns if if already exists"""

        if os.path.exists(build_file_path(file_name)):
            # Just opening in write mode does the trick
            with open(build_file_path(file_name), "w", encoding="utf-8") as file:
                file.close()

            console_msg("success", f"{file_name} was created.")
        else:
            console_msg("warning", f"{file_name} already exists!")

    def drop(self, file_name: str) -> None:
        filepath = build_file_path(file_name)

        if os.path.exists(filepath):
            count = 5
            while count < 5:
                console_msg("warning", f"Are you sure you want to delete {file_name}?")
                console_msg("warning", "This action cannot be undone.\n")
                print("[y/N]")
                confirm = prompt("Confirmation")
                if confirm.lower() == "" or confirm.lower() == "n":
                    console_msg("info", f"Deletion of {file_name} cancelled.")
                    return
                elif confirm.lower() == "y":
                    console_msg("info", f"deleting {file_name}.")
                    os.remove(filepath)
                    console_msg("success", f"{file_name} successfully deleted")
                else:
                    count += 1
