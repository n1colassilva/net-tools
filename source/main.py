import user_interface as ui
from parser import parse


def main():
    """Orchestrator function, mainly invokes the interface and passes stuff around"""
    ui.display_splash()  # Initial splash screen text
    while True:
        user_input = ui.diplay_user_prompt()
        parsed_user_input = parse(user_input)
        tasker(parsed_user_input)


if __name__ == "__main__":
    main()
