from classes.cli import Cli
from utils.console_messages import console_msg
from utils.fira_code_loading_bar.loading_bar import (
    generate_loading_bar as loading_bar,
)
from utils.manyprint.mprint import multi_print as printm
from ping3 import ping  # TODO make pylance stop complaining about lack of a stub


def _send_ping_request(destination_ip: str, count: int = 4, timeout: int = 30):
    received_packets = 0
    packet_loss = 0

    for _ in range(count):
        response = ping(destination_ip, timeout=timeout)

        if response is not None:  # TODO reffer to line 3's TODO
            print(f"Received ICMP response from {destination_ip} in {response} ms")
            received_packets += 1
        else:
            print("Request timed out")
            packet_loss += 1

    packet_loss_percentage = (packet_loss / count) * 100 if count > 0 else 0

    return destination_ip, count, received_packets, packet_loss, packet_loss_percentage


def ping_ip(ip_addresses: list[str], verbose: bool = False, amount: int = 4) -> None:
    """
    Sends an ICMP echo request to the designated adress(es)

    Args:
        ip_adresses (str): single or multiple ip adresses to ping
        verbose (bool, optional): Verbose mode shows more details. Defaults to False.
        amount (int, optional): Use in case you ever want to send more packets. Defaults to 4.
    """
    for ip in ip_addresses:
        (
            destination_ip,
            count,
            received_packets,
            packets_lost,
            packet_loss_percentage,
        ) = _send_ping_request(ip, amount)

        # printing the result
        if verbose is True:
            # TODO: colorize numbers according to how bad they are
            printm(
                "",
                "RESULTS:",
                f"Pinged: {destination_ip}",
                f"Sent: {count}",
                f"Recieved: {received_packets}",
                f"Packets lost: {packets_lost}",
                f"Packet loss: {packet_loss_percentage}%",
                loading_bar(count - packets_lost, count, 10),
            )
        else:
            printm(
                "",
                "RESULTS",
                f"Pinged: {destination_ip}",
                f"Packet loss: {packet_loss_percentage}%",
                loading_bar(count - packets_lost, count, 10),
            )


def run(data: Cli.CommandData):
    """Runs the icmp_scan function, the arguments are passed by the Cli's tasker"""

    # detecting our flags
    verbose: bool = False
    amount: int = 4
    # The function specifies these defaults but we are also setting them here to be sure
    for flag in data.flags:
        match flag.flag_type.long_name.lower():
            case "--verbose":
                verbose = True
                data.flags.pop()
                continue
            case "--amount":
                if flag.args_list is None:
                    console_msg(
                        "error",
                        "No amount of pings specified, continuing with default of 4",
                    )
                    break
                if flag.args_list[0] == "0":
                    console_msg(
                        "error",
                        "Why would you ask for 0 pings, continuing with default of 4",
                    )
                    break
                try:
                    amount = int(flag.args_list[0])
                except ValueError:
                    console_msg(
                        "error", "Type error: Amount expects an integer, continuing"
                    )
                    console_msg(
                        "hint", "Use `help chip` to learn how each argument works"
                    )
            case _:
                console_msg("error", f"Nonexistant flag detected, aborting")
                return
    # Everything should be set
    ping_ip(data.args, verbose, amount)


def register(Cli: Cli):
    command = Cli.Command()
    command.set_function("chip", run, "Sends an ICMP request to the determined host")
    command.set_argument("IP adresses", list[str], None)
    command.set_flag("-v", "--verbose", 0, bool, "Sets verbose mode to `true`")
    command.set_flag("-a", "--amount", 1, int, "Determines how many ICMP pings to send")
    Cli.register_command(command)

