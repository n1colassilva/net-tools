import getpass
import os
from typing import Optional
from termcolor import colored as clr
from utils.manyprint.mprint import multi_print as mprint

VERSION_NUMBER = "0.0.3"
VERSION_NAME = f"{clr('Alpha', 'green', attrs=['bold'])}"


# Show splash screen
def display_splash():
    """Prints out the splash screen"""
    print(clr("* NET TOOLS *", "black", "on_white", ["bold"]))
    print(f"Version {VERSION_NUMBER} {VERSION_NAME}")
    print("")
    print("MIT license")
    print("Copyright(c) Nícolas Sousa, 2024")
    print("\n")
    print(f"Type {clr('`help`','green' )} to see available commands\n")
    print("")


def display_user_prompt(_app_name: Optional[str] = "") -> str:
    """
    Displays a writing prompt for the user

    returns:
        str: The raw string the user typed in
    """
    username = getpass.getuser()
    domain = os.getenv("USERDOMAIN")
    # In case of no domain assume we are at home
    if isinstance(domain, type(None)):
        domain = "Home"
    print(
        f"\n{clr(username, 'blue', attrs=['bold'])}"
        " @ "
        f"{clr(domain,'magenta',attrs=['bold'])}"
    )
    print(_app_name, "> ", end="")

    user_input = input()
    print("")

    return user_input


# Show help menu
def display_help(arguments: list[str]):
    mprint(
        "",
        f"Net-tools {VERSION_NUMBER} {VERSION_NAME}",
        "",
        f"{clr('Commands:',attrs=['bold'])}",
        "`chip`    Check IP",
        "`chil`    Check IP list",
        "`help`    Help menu",
        "`exit`    Exits the program",
        "",
        "`Use `help [program name]` to learn specifics",
    )
