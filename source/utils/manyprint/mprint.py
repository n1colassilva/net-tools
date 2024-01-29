"""
Module with a single function, multi_print, for creating easier multiline print statements
"""


def multi_print(*strings: str, end: str = "\n"):
    """
    Simple function for printing multiple spaced lines

    Args:
        end (str, optional): _description_. Defaults to "\n"(newline).
    """
    for string in strings:
        print(string, end=end)
