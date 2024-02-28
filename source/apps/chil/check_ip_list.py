from termcolor import colored as clr
import sys
from apps.chil.lib.chil_data_print import dorlprint

sys.path.append("../../../../source")
from apps.chil.lib.ip_list import load_toml, add_entry
from utils.manyprint.mprint import multi_print as printm
from utils import console_messages
from utils.console_messages import console_msg
from user_interface import display_user_prompt as prompt
from tasker import input_parser

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
        
        self.display_name = (
            self.APP_NAME +
            " 󰁔 " +
            clr("󰏪", "green") +
            " " +
            clr("" + self.file_name, "black", "on_white")
        )

        usr_dict:dict[str,str]

        command:str= ""
        while command != "done":
            usr_input = prompt(self.display_name)

            command, args = input_parser(usr_input)

            match command:
                case "done":
                    # here we break because the while will handle it
                    break
                case "ip":
                    usr_dict 
