from apps.chil.check_ip_list import ChilTerm
from apps.chip.ip_scan import icmp_scan
from user_interface import display_help
from utils.console_messages import console_msg
from utils.input_parser import input_parser


def task(usr_input: str):
    """Runs the program the user input tells it to"""
    # Parsing the user input
    command, arguments = input_parser(usr_input)

    match command:
        case "chip":
            verbose: bool = False
            amount: int = 4
            ip_addresses: list[str] = []

            i = 0
            while i < len(arguments):
                argument = arguments[i]

                match argument:
                    case "-v" | "--verbose":
                        verbose = True

                    case "-a" | "--amount":
                        # Check if there's a next argument
                        if i + 1 < len(arguments):
                            amount = int(arguments[i + 1])
                            # Remove both the flag and its argument
                            arguments.pop(i)
                            arguments.pop(i)  # Pop again to remove the argument
                        else:
                            console_msg("error", "Missing value for --amount")

                    case _:
                        if argument.startswith("-"):
                            console_msg("error", f"Unknown flag: {argument}")
                        else:
                            ip_addresses.append(argument)

                i += 1

            icmp_scan(ip_addresses, verbose, amount)
        case "chil":
            chilterm = ChilTerm()
            chilterm.run()

        case "help":
            display_help(arguments)

        case "exit":
            console_msg("info", "Exiting net-tools.")
            exit(0)
        case _:
            console_msg("error", "Unknown command")
