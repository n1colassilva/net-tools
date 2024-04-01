"""
Module for printing errors, warnings and hints
"""

from typing import Literal
from termcolor import colored

# This is to help intellisense
Tag = Literal["success", "hint", "info", "warning", "error"]

TAGS: dict[Tag, str] = {
    "success": colored("SUCCESS:", "white", "on_green"),
    "hint": colored("HINT:", "white", "on_blue"),
    "info": colored("INFO:", "white", "on_blue"),
    "warning": colored("WARNING:", "white", "on_yellow"),
    "error": colored("ERROR:", "white", "on_red"),
}


# msg standing for MeSsaGe and not MonoSodium Glutamate
def console_msg(tag: Tag, message: str) -> None:
    """
    general purpose console message printer function.

    ## args:
        tag (tag): Tag for the message
        message (str): Message string (as in what you want the console to say).

    ## available tags:
        - `success`: Indicates to a user that an operation was successfull, you can include more information like what was associated to what;
        - `hint`: Usually just tells that you can use help, but can also give other hints as how to use commands better (like after a weird error);
        - `info`: May follow success,warning or an error, indicating what went wrong where;
        - `warning`: Indicated something will or could go wrong, not really catastrophic but the user should watch their step;
        - `error`: Something went horribly wrong, the operation is cancelled.
    """
    # I totally didnt copy this from how termcolor is structured
    # (tbf they used a separate types file) # i dont think it justifies
    # This looks horrendous but its just grabbing the premade tag string and shoving it in there # It's not that bad what was i thinking
    print(f"{TAGS[tag]} {message}")


# def hint(message: str):
#     """Prints a hint"""
#     print("")
#     print(colored("HINT:", "white", "on_blue"), end=" ")
#     print(message)


# def warning(message: str):
#     """Prints a warning"""
#     print("")
#     print(colored("WARNING:", "white", "on_yellow"), end=" ")
#     print(message)


# def error(message: str):
#     """Prints an error"""
#     print("")
#     print(colored("ERROR:", "white", "on_red"), end=" ")
#     print(message)
