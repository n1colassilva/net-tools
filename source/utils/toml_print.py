from typing import Any


def toml_data_print(tdict: dict[str, Any], _indent: int = 0):
    """
    Prints a nested dictionary with indentation for readability.

    Args:
        tdict (dict[str, Any]): The nested dictionary to be printed.
        _indent (int, optional): The indentation level (for internal use). Defaults to 0.
    """
    for key, value in tdict.items():
        if isinstance(value, dict):
            print(" " * _indent, key + ":")
            # Increase indentation for nested elements
            toml_data_print(value, _indent + 2)  # type: ignore - pylance cares too much about the type of value
        else:
            print(" " * _indent, key, ":", value)
