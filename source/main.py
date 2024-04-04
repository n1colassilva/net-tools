from classes.cli import Cli
import user_interface as ui
from apps.app_register import register_all as register_apps


def main():
    """Orchestrator function, mainly invokes the interface and passes stuff around"""

    ui.display_splash()  # Initial splash screen text

    main_cli = Cli("")
    register_apps(main_cli)
    main_cli.run()

if __name__ == "__main__":
    main()
