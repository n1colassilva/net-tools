# from tasker import task
from classes.cli import Cli
import user_interface as ui


def main():
    """Orchestrator function, mainly invokes the interface and passes stuff around"""

    ui.display_splash()  # Initial splash screen text

    main_cli = Cli("")
    main_cli.run()

if __name__ == "__main__":
    main()
