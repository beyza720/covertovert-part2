import scapy.all as scapy
import time
from CovertChannelBase import CovertChannelBase

class MyCovertChannel(CovertChannelBase):
    """
    - You are not allowed to change the file name and class name.
    - You can edit the class in any way you want (e.g. adding helper functions); however, there must be a "send" and a "receive" function, the covert channel will be triggered by calling these functions.
    """
    def __init__(self):
        """
        - You can edit __init__.
        """
        super().__init__()
        self.received_message = ""
        self.previous_time = None
        self.destination = "receiver"

    def send(self, log_file_name, wait_0, wait_1):
        """
        - In this function, you expected to create a random message (using function/s in CovertChannelBase), and send it to the receiver container. Entire sending operations should be handled in this function.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        binary_message = self.generate_random_binary_message_with_logging(log_file_name)

        start_time = time.time()

        self.send_packets(binary_message, wait_0, wait_1)

        end_time = time.time()

        capacity = len(binary_message) / (end_time - start_time)
        print(capacity)

    def send_packets(self, binary_message, wait_0, wait_1):
        
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
        - In this function, you are expected to receive and decode the transferred message. Because there are many types of covert channels, the receiver implementation depends on the chosen covert channel type, and you may not need to use the functions in CovertChannelBase.
        - After the implementation, please rewrite this comment part to explain your code basically.
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
