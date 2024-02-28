import getpass
import os
from typing import Optional
from termcolor import colored as clr


# Show splash screen
def display_splash():
    """Prints out the splash screen"""
    print(clr("* NET TOOLS *", "black", "on_white", ["bold"]))
    print(f"Version 0.0.2 {clr("alpha","green")}")
    print("")
    print("MIT license")
    print("Copyright(c) Nícolas Sousa, 2024")
    print("\n")  # 3 empty lines
    print(f"Type {clr("'help'","green" )} to see available commands\n")
    print("")

def display_user_prompt(_app_name:Optional[str]="") -> str:
    """
    Displays a writing prompt for the user
    
    returns:
        str: The raw string the user typed in
    """
    username = getpass.getuser()
    domain = os.getenv("USERDOMAIN")
    # In case of no domain assume we are at home
    if isinstance(domain,type(None)):
        domain = "Home"
    print(
        f"\n{clr(username, "blue", attrs=["bold"])}"
        " @ "
        f"{clr(domain,"magenta",attrs=["bold"])}"
    )
    print(_app_name, "> ",end="")

    user_input = input()
    print("")

    return user_input



# Show main menu


# Show help menu
def display_help():
    ...
