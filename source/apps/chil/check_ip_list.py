from termcolor import colored as clr
import sys

sys.path.append("../../../../source")
from apps.chil.lib.ip_list import load_toml, add_entry
from utils.manyprint.mprint import multi_print as printm
from utils import console_messages
from utils.console_messages import console_msg
from user_interface import diplay_user_prompt as prompt
from tasker import input_parser

class ChilTerm():
    """
    TODO
    """
    def __init__(self):
        self.file_name:str = ""

    def run(self):
        """Main terminal loop"""

        # Show splash screen
        self._splash()

        keep_running = True

        while keep_running:

            # We will append the file name onto the app name to show user current file
            # inlay hints may give you an aneurism
            app_name = f"{clr("chil 󰻽","white","on_blue",["bold"])}"
            full_path = app_name + self.file_name

            user_input = prompt(full_path)

            command, arguments = input_parser(user_input)

            match command:
                case "select":
                    self.select_file(arguments[0])
                case "view":
                    ...
                case "insert":
                    ...
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
        printm(
            f"{clr(" " + self.file_name,"cyan")}"
            "",
            "----------",
            "----------",
            "",
        )


# class chil:
#     """prototype"""

#     def __init__(self) -> None:
#         # self.filename = select_file()
#         ...

#     def select_file(self):
#         """Placeholder"""

#     def show_in_editor(self):
#         """placeholder"""

#     def insert(self, _data: str):
#         """placeholder"""

#     def remove(self, _ip: str):
#         """placeholder"""

#     def create(self, _filename: str):
#         """placeholder"""

#     def delete(self, _filename: str):
#         """placeholder"""
