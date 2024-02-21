"""
Module for printing errors, warnings and hints
"""
from typing import Literal
from termcolor import colored

# This is to help intellisense
Tag = Literal["hint", "warning", "error"]

TAGS: dict[Tag, str] = {
    "hint": colored("HINT:", "white", "on_blue"),
    "warning": colored("WARNING:", "white", "on_yellow"),
    "error": colored("ERROR:", "white", "on_red"),
}


# msg standing for MeSsaGe and not MonoSodium Glutamate
def console_msg(tag: Tag, message: str):
    """
    general purpose console message printer function.

    args:
        tag (tag): Tag for the message
        message (str): Message string (as in what you want the console to say).

    available tags:
        hint, warning, error.
    """
    # I totally didnt copy this from how termcolor is structured
    # (tbf they used a separate types file)
    # This looks horrendous but its just grabbing the premade tag string and shoving it in there
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
