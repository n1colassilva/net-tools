import yaml


def parse(string: str):
    """
    Parses a string into it's arguments, flags, flag arguments and commands.

    Args:
        string (str): user input string.
    """
    input_list = string.split(" ")
    command = input_list.pop(0)

    # pretend we took the command, looked through the metadata files and found the correct function
    file_path = "source\\apps\\chip\\metadata.yaml"
    with open(file_path, "r", encoding="utf-8") as file:
        #
        # expected structure for yaml data

        # name: str
        # description: str
        # flags:
        #     -f/--foo:
        #         value: any (value we will look for)
        #         description: str
        #     -b/--bar:
        #          value:
        #          ...
        yaml_data = yaml.safe_load(file)

    name = yaml_data.get("name")
    flag_names = yaml_data["flags"].keys()
    flags = yaml_data.get("flags")

    #if command matches the name
    if command != name:
        return None
    #for every word the user input
    for i,input in enumerate(input_list):
        for flag in flag_names:
            if input != flag:
                continue
            flag_data = flags.get(flag)




if __name__ == "__main__":
    parse("chip -a 5 192.168.0.14")
