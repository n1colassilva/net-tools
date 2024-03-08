import ipaddress
from termcolor import colored as clr
from ...tasker import input_parser

from source.apps.chil.lib.ip_list import build_file_path, load_toml, add_entry
from source.apps.chil.lib.chil_data_print import dorlprint
from source.utils.manyprint.mprint import multi_print as printm
from source.utils.console_messages import console_msg
from source.user_interface import display_user_prompt as prompt

class ChilTerm():
    """
    TODO
    """
    def __init__(self):
        self.file_name:str = ""
        self.APP_NAME = f"{clr("chil 󰻽","white","on_blue",["bold"])}"
        self.display_name = self.APP_NAME

    def run(self):
        """Main terminal loop"""

        # Show splash screen
        self._splash()

        keep_running = True

        while keep_running:

            if self.file_name != "":
                self.display_name = (
                    self.APP_NAME +
                    " 󰁔 " +
                    "" +
                    clr(self.file_name, attrs=["bold"])
                )

            user_input = prompt(self.display_name)
            command, arguments = input_parser(user_input)

            match command:
                case "select":
                    self.select_file(arguments[0])
                case "view":
                    self.display_file()
                case "insert":
                    self.insert() # A writing/fanfic joke goes here.
                case "remove":
                    ...
                case "create":
                    ...
                case "drop":
                    ...
                case _:
                    ...


    def _splash(self):
        """Prints chil's own splash screen"""
        printm(
            "'chil󰻽': Check IP List",
            "App for managing TOML files containig an ip list",
            "",
            "MIT license",
            "󰗦 Nícolas 2024",
            "",
            f"Type {clr("'help'","green" )} to see available commands\n"
        )


    def select_file(self, file_name:str):
        """Tries to find the toml and sets it as file_name"""
        data = load_toml(file_name)
        if data is None:
            console_msg("hint","Use 'show-dir' to see all existant files")
        else:
            self.file_name = file_name


    def display_file(self):
        """Shows a file's data"""
        data = load_toml(self.file_name)

        if data is None:
            console_msg("error","Empty file.")
            return

        printm(
            f"{clr(" " + self.file_name,"cyan")}"
            "",
            "----------",
            dorlprint(data),
            "----------",
            "",
        )


    def insert(self):
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
            self.APP_NAME +
            " 󰁔 " +
            clr("󰏪", "green") +
            " " +
            clr("" + self.file_name, "black", "on_white")
        )

        usr_dict:dict[str,str] = {}

        command:str= ""
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
                        console_msg("error","Invalid ip adress")
                    finally:
                        usr_dict["ip"] = args[0]
                case "name":
                    usr_dict["name"] = args[1]
                case "description":
                    usr_dict["description"] = " ".join(args)
                case "custom":
                    usr_dict[args[0]] = args[1]
                case "write":
                    write_path = build_file_path(args[1])
                    add_entry(write_path,usr_dict)
                    command = "none" # A little hacky but will get the job done
                case _:
                    console_msg("error", "Invalid input.")
                    console_msg("hint", "Use 'help' to learn more")
