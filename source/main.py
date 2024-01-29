import sys
from termcolor import colored as clr
import user_interface as ui
from console_messages import console_msg
from ip_scan import icmp_scan


def main():
    ui.display_splash()  # Initial splash screen text
    while True:
        user_input = ui.diplay_user_prompt()

        arguments = user_input.split()

        match arguments[0]:
            case "help":
                if arguments[1] == "":
                    ui.display_help()
                else:
                    ...  # todo advanced help implementation

            case "scan":
                match arguments[1]:
                    case "ip":
                        # ICMP the arguments[2]
                        # Todo flag implementation
                        icmp_scan(arguments[2])

                    case "range":
                        # ICMP from arguments[2] to arguments[3]
                        # check if there is a arguments[3]
                        if arguments[3] == "":
                            console_msg("error", "Second ip not passed")
                            console_msg(
                                "hint",
                                "Type 'scan help' to learn about the scan functions",
                            )
                    case "help":
                        # Show relevant help
                        ...
                    case _:
                        console_msg("error", "No specified 'scan' function.")
                        console_msg(
                            "hint", "Type 'scan help' to learn about the scan functions"
                        )
            case "exit":
                sys.exit(0)
            case _:
                print(clr(f"{arguments[0]} is not a valid command", "green"))
                console_msg("hint", "Type 'help' to see available commands")


if __name__ == "__main__":
    main()
