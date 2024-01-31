import re


def parse_command_string(command_string: str):
    # Define a regular expression pattern to match the command format
    pattern = re.compile(
        r"(?P<program>\w+)(?:\s+(?P<subprogram>\w+))?(\s+-f\s+(?P<flag_arg>\w+))?(\s+(?P<args>[\w\s]+))?"
    )

    # Match the pattern against the command string
    match = pattern.match(command_string)

    if match:
        # Extract matched groups
        program = match.group("program")
        subprogram = match.group("subprogram")
        flag_arg = match.group("flag_arg")
        args = match.group("args")

        # Split multiple arguments if present
        args_list = args.split() if args else []

        return {
            "program": program,
            "subprogram": subprogram,
            "flag_arg": flag_arg,
            "args": args_list,
        }
    else:
        return None


# Example usage:
command_string = "my_program my_subprogram -f flag_value arg1 arg2 arg3"
result = parse_command_string(command_string)

if result:
    print("Parsed Result:")
    print(result)
else:
    print("Invalid command string format.")
