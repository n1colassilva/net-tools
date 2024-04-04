from typing import Callable
from classes.cli import Cli

"""
Instructions:

1. In your app make a function to register your function, it must take in a Cli.
    1.1. Register the command;
    1.2. Register it's args;
    1.3. Register it's flags.

2. Import your app's file where your  registering function.
    2.1. You should not import just the register function so it's easier to tell where
    the register function came from.

3. Add the register function to the apps list.
"""
from .chip import ip_scan as ipscan

apps: list[Callable[[Cli], None]] = [
    ipscan.register,
]


def register_all(Cli: Cli):
    """Runs through each app's register function and runs each to save it to the  cli"""
    for registerable in apps:
        registerable(Cli)
