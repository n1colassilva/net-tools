import socket
import struct
import time
from utils.fira_code_loading_bar.loading_bar import generate_loading_bar as loading_bar
from utils.manyprint.mprint import multi_print as printm


def _send_ping_request(destination_ip: str, count: int = 4, timeout: float = 30):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    icmp_header = struct.pack("!BBHHH", 8, 0, 0, 1, 1)
    icmp_checksum = 0
    icmp_packet = icmp_header + struct.pack("H", icmp_checksum) + b"HelloPing"

    received_packets = 0
    packet_loss = 0

    for _ in range(count):
        icmp_socket.sendto(icmp_packet, (destination_ip, 1))

        icmp_socket.settimeout(timeout)

        try:
            start_time = time.time()
            _response, addr = icmp_socket.recvfrom(1024)
            end_time = time.time()

            round_trip_time = (end_time - start_time) * 1000  # Convert to milliseconds
            print(f"Received ICMP response from {addr[0]} in {round_trip_time:.2f} ms")
            received_packets += 1
        except socket.timeout:
            print("Request timed out")
            packet_loss += 1

    icmp_socket.close()

    packet_loss_percentage = (packet_loss / count) * 100 if count > 0 else 0

    return destination_ip, count, received_packets, packet_loss, packet_loss_percentage

    # {
    #     "destination_ip": destination_ip,
    #     "sent_packets": count,
    #     "received_packets": received_packets,
    #     "packet_loss": packet_loss,
    #     "packet_loss_percentage": packet_loss_percentage,
    # }


def icmp_scan(*ip_addresses: str, verbose: bool = False, amount: int = 4) -> None:
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
            recieved_packets,
            packets_lost,
            packet_loss_percentage,
        ) = _send_ping_request(ip, amount)

        # printing the result
        if verbose is True:
            # TODO: colorize numbers according to how bad they are
            printm(
                "RESULTS:",
                f"Pinged: {destination_ip}",
                f"Sent: {count}",
                f"Recieved: {recieved_packets}",
                f"Packets lost: {packets_lost}",
                f"Packet loss: {packet_loss_percentage}%",
                loading_bar(packets_lost, count, count * 2),
            )
        else:
            printm(
                "RESULTS",
                f"Pinged: {destination_ip}",
                f"Packet loss: {packet_loss_percentage}%",
                loading_bar(packets_lost, count, count * 2),
            )
