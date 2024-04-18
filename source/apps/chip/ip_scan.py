from socket import timeout
from classes.cli import Cli
from classes.ip import IPAddress
from utils.console_messages import console_msg
from utils.fira_code_loading_bar.loading_bar import (
    generate_loading_bar as loading_bar,
)
from utils.manyprint.mprint import multi_print as printm
from ping3 import ping  # TODO make pylance stop complaining about lack of a stub


def _send_ping_request(
    destination_ip: str,
    count: int = 4,
    size: int = 64,
    timeout: int = 30,
    verbose: bool = False,
):
    """
    Sends an ICMP ping request to the chosen host.

    Args:
        destination_ip (str): Chosen host, in IP form.
        count (int, optional): Amount of pings to send. Defaults to 4.
        size (int, optional): Size in bytes of the ICMP packet. Defaults to 64
        timeout (int, optional): How long to wait for a response for each ping. Defaults to 30.
        verbose (bool, optional): Shows more detailed output. Defaults to False.

    Returns:
        None or Tuple(str, int, int, int, float): Data from the ping response, like how many packets were sent, received, lost etc, in case of failure returns None.
    """
    received_packets = 0
    packet_loss = 0

    adress = IPAddress(destination_ip)
    if not adress.is_valid():
        console_msg("error", f"Invalid IP adress '{adress}, aborting")
        return None
    for _ in range(count):
        if verbose:
            console_msg("info", f"Pinging {destination_ip} with {size}B")
        response = ping(destination_ip, timeout=timeout)

        if response is not None:  # TODO reffer to line 3's TODO
            if verbose:
                console_msg("info", f"Response from {destination_ip}, time: {response}")
            else:
                console_msg(
                    "info", f"Received response from {destination_ip} in {response} ms"
                )
            received_packets += 1
        else:
            print("Request timed out")
            packet_loss += 1

    packet_loss_percentage = (packet_loss / count) * 100 if count > 0 else 0

    return destination_ip, count, received_packets, packet_loss, packet_loss_percentage


def ping_ip(
    ip_addresses: list[str], verbose: bool, amount: int, timeout: int, size: int
) -> None:
    """
    Sends an ICMP echo request to the designated adress(es)

    Args:
        ip_adresses (str): single or multiple ip adresses to ping
        verbose (bool, optional): Verbose mode shows more details.
        amount (int, optional): Use in case you ever want to send more packets. Defaults to 4.
        timeout (int, optional): How long to wait for a response for each ping
        size (int, optional): Size of the packet to send.
    """
    for ip in ip_addresses:
        result = _send_ping_request(ip, amount, size, timeout, verbose)
        if result is None:
            return  # _send_ping_request handles this
        else:
            (
                destination_ip,
                count,
                received_packets,
                packets_lost,
                packet_loss_percentage,
            ) = result

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
                loading_bar(count - packets_lost, count, 30),
                "",
            )
        else:
            printm(
                "",
                "RESULTS",
                f"Pinged: {destination_ip}",
                f"Packet loss: {packet_loss_percentage}%",
                loading_bar(count - packets_lost, count, 30),
                "",
            )


def run(data: Cli.CommandData):
    """Runs the icmp_scan function, the arguments are passed by the Cli's tasker"""

    # detecting our flags

    # TODO: find a better way to enforce defaults
    verbose: bool = False
    amount: int = 4
    timeout: int = 30
    size: int = 64

    for flag in data.flags:
        match flag.flag_type.long_name.lower():
            case "--verbose":
                verbose = True
                continue
            case "--amount":
                if flag.args_list is None:
                    console_msg(
                        "error",
                        "No amount of pings specified, continuing with default of 4",
                    )
                    continue
                if flag.args_list[0] == "0":
                    console_msg(
                        "error",
                        "Why would you ask for 0 pings, continuing with default of 4",
                    )
                    continue
                try:
                    amount = int(flag.args_list[0])
                except ValueError:
                    console_msg(
                        "error", "Type error: Amount expects an integer, continuing"
                    )
                    console_msg(
                        "hint", "Use `help chip` to learn how each argument works"
                    )

            case "--timeout":
                if flag.args_list is None:
                    console_msg(
                        "error",
                        "No value provided of timeout flag. Continuing with default.",
                    )
                    timeout = 30
                    continue
                try:
                    timeout = int(flag.args_list[0])
                    continue
                except ValueError:
                    console_msg(
                        "error",
                        "Type error: timeout expects an integer, continuing with timeout of 30",
                    )
                    timeout = 30
                    continue

            case "--size":
                if flag.args_list == None:
                    console_msg(
                        "error",
                        "No value provided for size flag, continuing with default",
                    )
                    size = 64
                    continue
            case _:
                console_msg("error", f"Nonexistant flag detected, aborting")
                return
    # Everything should be set
    ping_ip(data.args, verbose, amount, timeout, size)


def register(Cli: Cli):
    command = Cli.Command()
    command.set_function("chip", run, "Sends an ICMP request to the determined host")
    command.set_argument("IP adresses", list[str], None)
    command.set_flag("-a", "--amount", 1, int, "Sets how many ICMP pings to send")
    command.set_flag("-v", "--verbose", 0, bool, "Sets verbose mode to `true`")
    command.set_flag("-t", "--timeout", 1, int, "Sets how long to wait for a response")
    command.set_flag("-s", "--size", 1, int, "Sets the size of the packets in bytes")
    Cli.register_command(command)
