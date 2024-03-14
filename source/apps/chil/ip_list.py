"""
Handles IO operations for check ip list (chil)
"""

from utils.console_messages import console_msg
from io import TextIOWrapper
import os
from typing import Literal, Optional
import toml


def build_file_path(file_name: str):
    """
    Makes sure the file path includes the extension and goes intot the correct folder
    Args:
        file_name (str)
    Returns:
        str: A path to the supposed file
    """
    if not file_name.endswith(".toml"):
        file_name += ".toml"

    file_path = os.path.join("/source/data/chil/ip_list", file_name)

    return file_path


# This is for intellisense to show what modes to use and make pylance stop complaining
OpenLiteral = Literal["r", "w"]


def _load_file(file_name: str, mode: OpenLiteral = "r") -> Optional[TextIOWrapper]:
    """
    Loads the file at the specified path.
    made to be used by `load_toml()` but can be used on it's own
    Args:
        file_path (str): The path to the file.
        mode (str, optional): The mode to open the file in. Defaults to "r".
    Returns:
        Optional[TextIOWrapper]: The file object if successful, else None.
    """

    file_path = build_file_path(file_name)

    try:
        with open(file_path, mode, encoding="utf-8") as file:
            return file

    except FileNotFoundError:
        console_msg("error", f"File '{file_path}' not found.")
        return None
    except Exception as e:
        console_msg("error", f"An error occurred while loading file '{file_path}': {e}")
        return None


def load_toml(
    file_name: str, _verbose: bool = False
) -> dict[str, dict[str, str]] | None:
    """
    Loads a TOML file.
    Args:
        file_name (str): The name of the file to load.
        _verbose (bool, optional): Whether to enable verbose mode. Defaults to False.
        _return_file (bool, optional): Whether to return the file object. Defaults to False.
    Returns:
        Union[dict, None]: The loaded data if successful, else None.
    """
    file_path = build_file_path(file_name)
    file = _load_file(file_path)
    if file:
        try:
            data = toml.load(file)
            return data
        except Exception as e:
            console_msg("error", f"An error occurred while parsing TOML data: {e}")
        finally:
            file.close()
    return None


def add_entry(file_name: str, entry: dict[str, str], _verbose: bool = False):
    """
    Adds a new entry to an ip list file.
    Args:
        file_name (str): The name of the file.
        entry (dict[str, str]): The entry to be added.
        _verbose (optional,bool): Whether verbose mode is enabled. Defaults to False
    """

    file_path = build_file_path(file_name)
    # Loading TOML data
    data = load_toml(file_path, _verbose)

    if data is not None:
        # If the "ip_addresses" table does not exist, create it now
        if "ip_addresses" not in data:
            data["ip_addresses"] = {"entry": "placeholder"}

        # Appending new entry to the "ip_addresses" table
        data["ip_addresses"]["entry"].append(entry)  # type: ignore

        # Writing the updated data back to the TOML file
        file = _load_file(file_path, "w")

        # Handle file open error
        if file is None:
            console_msg("error", "Failed to open file for writing")
            return False

        try:
            toml.dump(data, file)
            return True  # Successfully added the entry
        except Exception as e:
            console_msg("error", f"An error occurred while writing to file: {e}")
            return False
        finally:
            file.close()
    else:
        console_msg("error", "Failed to load TOML data")
        return False
