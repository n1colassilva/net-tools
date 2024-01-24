"""
Module for printing errors, warnings and hints
"""
from termcolor import colored


def hint(message: str):
    """Prints a hint"""
    print(colored("HINT:", "white", "on_blue"), end=" ")
    print(message)


def warning(message: str):
    """Prints a warning"""
    print(colored("WARNING:", "white", "on_yellow"), end=" ")
    print(message)


def error(message: str):
    """Prints an error"""
    print(colored("ERROR:", "white", "on_red"), end=" ")
    print(message)
