"""
General purpose command parser
"""


def parse(user_input: str):
    """
    Grabs the main command and makes a list of all arguments
    """
    arguments = user_input.split(" ")

    command = arguments.pop(0)

    return command, arguments
