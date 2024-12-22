import scapy.all as scapy
import time
from CovertChannelBase import CovertChannelBase

class MyCovertChannel(CovertChannelBase):
    """
   This class implements a covert timing channel using ICMP packets.
    
    - The `send` function generates and transmits a binary message to a receiver by manipulating packet inter-arrival times.
    - The `receive` function listens for incoming ICMP packets and decodes the binary message based on the inter-arrival time.
    - A termination condition is implemented to stop message transmission or reception when a specific signal (e.g., a dummy packet or a "." character) is detected.
    """
    def __init__(self):
        """
        - Initializes the covert channel with necessary variables.
        - `self.received_message`: Stores the binary representation of the received message.
        - `self.previous_time`: Tracks the time of the previous packet to calculate inter-arrival time.
        - `self.destination`: Destination IP address or hostname for the receiver.
        """
        super().__init__()
        self.received_message = ""
        self.previous_time = None
        self.destination = "receiver"

    def send(self, log_file_name, wait_0, wait_1):
        """
        - Generates a random binary message and sends it to the receiver using ICMP packets.
        - Logs the binary message to the specified log file.
        - Uses `send_packets` to handle the actual packet transmission with delays corresponding to binary bits.
        """
        binary_message = self.generate_random_binary_message_with_logging(log_file_name)

        start_time = time.time()

        self.send_packets(binary_message, wait_0, wait_1)

        end_time = time.time()

        capacity = len(binary_message) / (end_time - start_time)
        print(capacity)

    def send_packets(self, binary_message, wait_0, wait_1):
        """
        - Sends ICMP packets based on the binary message.
        - Delays between packet transmissions represent binary `0` and `1`.
        - A dummy packet is sent at the end to indicate termination.
        """
        for bit in binary_message:
            # create the packet
            packet = scapy.IP(
                dst = self.destination,
                ttl = 1
            )

            # make packet icmp
            packet = packet / scapy.ICMP()

            # send packet
            super().send(packet)

            if bit == "0":
                time.sleep(wait_0)
            else:
                time.sleep(wait_1)

        # create dummy packet to terminate
        dummy_packet = scapy.IP(
            dst = self.destination,
            ttl = 1
        )
        
        # make packet icmp
        dummy_packet = dummy_packet / scapy.ICMP()

        # send packet
        super().send(dummy_packet)

        
    def receive(self, log_file_name, bound_0, bound_1):
        """
        - Receives ICMP packets and decodes the binary message based on inter-arrival times.
        - Appends decoded bits to `self.received_message` and stops on receiving a dummy packet or "." character.
        - Logs the final decoded message to the specified log file.
        """
        while True:
            # wait for the packet
            packet = scapy.sniff(
                filter = 'icmp',
                count=1
            )[0]

            # get current time
            current_time = time.time()

            if self.previous_time is not None:
                inter_arrival_time = current_time - self.previous_time

                if inter_arrival_time < bound_0 and inter_arrival_time > bound_1:
                    self.received_message += "0"
                elif inter_arrival_time < bound_1:
                    self.received_message += "1"
                else:
                    # stop due to long delay
                    print('STOPPED DUE TO LONG DELAY')
                    break

            self.previous_time = current_time

            if len(self.received_message) > 0 and len(self.received_message) % 8 == 0:
                last_byte = self.received_message[-8:]
                last_char = super().convert_eight_bits_to_character(last_byte)

                if last_char == ".":
                    break
            
        
        message = ""

        for i in range(0, len(self.received_message), 8):
            curr_byte = self.received_message[i:i+8]
            curr_char = super().convert_eight_bits_to_character(curr_byte)

            message += curr_char


        self.log_message(message, log_file_name)
