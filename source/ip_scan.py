import ipaddress
import socket
import struct
import time


def _send_ping_request(destination_ip: str, count: int = 4, timeout: float = 1):
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

    result = {
        "destination_ip": destination_ip,
        "sent_packets": count,
        "received_packets": received_packets,
        "packet_loss": packet_loss,
        "packet_loss_percentage": packet_loss_percentage,
    }

    return result


from ip import IPAddress
from typing import Union


def icmp_scan(*ip_adress: IPAddress, **flags: Union[bool, int]):
    verbose: bool = flags.get("verbose", False)
    amount: int = flags.get("amount", 1)
    # continuous: bool = flags.get("continuous", False)
