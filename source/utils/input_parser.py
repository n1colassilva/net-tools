def input_parser(usr_input: str) -> tuple[str, list[str]]:
    """Divides input into the main command and it's arguments"""
    arguments = usr_input.split(" ")
    command = arguments.pop(0)
    return command, arguments