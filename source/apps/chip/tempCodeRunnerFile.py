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