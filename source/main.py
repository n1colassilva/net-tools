from parsing import parse
from tasker import task
import user_interface as ui


def main():
    """Orchestrator function, mainly invokes the interface and passes stuff around"""

    ui.display_splash()  # Initial splash screen text

    while True:

        user_input = ui.diplay_user_prompt()

        command, arguments = parse(user_input)

        task(command, arguments)


if __name__ == "__main__":
    main()
