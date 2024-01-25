import getpass
import os
from termcolor import colored as clr


# Show splash screen
def display_splash():
    """Prints out the splash screen"""
    print(clr(" NET TOOLS ", "black", "on_white"))
    print(f"Version 0.0.1 {clr("alpha","green")}")
    print("")
    print("MIT license")
    print("Copyright(c) Nícolas Sousa, 2024")
    print("\n")  # 3 empty lines
    print(f"Type {clr("'help'","green" )} to see available commands\n")
    print("")

def diplay_user_prompt():
    username = getpass.getuser()
    domain = os.getenv("USERDOMAIN")
    
    # In case of no domain assume we are at home
    if isinstance(domain,type(None)):
        domain = "Home"
    
    print(
        f"{username} @ {domain}"
    )
    print(">",end="")




# Show help menu
def display_help():
    ...


# Show main menu
# def display_menu():

# Show ip scan interface

# Show ip scan results

# Show free ip interface

# Show free ip results
