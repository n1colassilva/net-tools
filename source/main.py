import source.user_interface as ui
import source.console_messages as console


def main():
    ui.display_splash()  # Initial splash screen text
    while True:
        user_input = input()

        user_input.split()

        match user_input[0]:
            case "help":
                if user_input[1] == "":
                    ui.display_help()
                else:
                    ...  # todo advanced help implementation

            case "scan":
                match user_input[1]:
                    case "ip":
                        # ICMP the user_input[2]
                        ...
                    case "range":
                        # ICMP from user_input[2] to user_input[3]
                        # check if there is a user_input[3]
                        if user_input[3] == "":
                            console.error("Second ip not passed")
                            console.hint(
                                "Type 'scan help' to learn about the scan functions"
                            )
                    case "help":
                        # Show relevant help
                        ...
                    case _:
                        console.error("No specified 'scan' function.")
                        console.hint(
                            "Type 'scan help' to learn about the scan functions"
                        )
