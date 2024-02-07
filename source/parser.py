from typing import Any, Dict, Union
import yaml

parsed_command: dict[str, str | dict[str, Any] | list[Any]] = {
    "command": command,
    "flags": {},
    "args": [],
}
class command_metadata:

    def __init__(self, name, flag_data) -> None:
        pass
    

def get_metadata() -> Dict[str, Union[str, Dict[str, Union[None, type, str]]]]:

    file_path = "source\\apps\\chip\\metadata.yaml"

    with open(file_path, "r", encoding="utf-8") as file:
        metadata = yaml.safe_load(file)

    # now we parse said metadata
        
    metadata.   

    return metadata


def parse_input(
    user_input: str, metadata: Dict[str, Union[str, Dict[str, Union[None, type, str]]]]
):

    inputs = user_input.split("")

    command = inputs.pop(0)

    # Defining our Abstract Syntax Tree
    parsed_command: dict[str, str | dict[str, Any] | list[Any]] = {
        "command": command,
        "flags": {},
        "args": [],
    }

    