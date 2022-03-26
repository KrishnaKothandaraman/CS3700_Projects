from typing import Dict, List, Tuple
import sys

Packet = Tuple[int, str]


def log(message):
    sys.stderr.write(message + "\n")
    sys.stderr.flush()


class SenderWindow:
    """Class that mimics TCP Sender Window"""
    buffer: List[str]
    last_sent: int
    last_successful_ack: int
    max_buffer_size: int
    received_acks = List[int]

    def __init__(self, max_buff):
        self.buffer = []
        self.last_sent = -1
        self.max_buffer_size = max_buff
        self.last_successful_ack = -1
        self.packets_in_network = 0
        self.received_acks = []

    def add_data(self, data: str) -> None:
        """Appends data to buffer"""
        self.buffer.append(data)

    def get_data_to_send(self) -> List[Packet]:
        """Gets all data that can be sent after taking into consideration packets that have been sent but are un
        acknowledged """
        if self.last_sent >= len(self.buffer):
            return []

        if self.last_sent == -1:
            last_transmissible_idx = min(self.max_buffer_size - self.packets_in_network + 1, len(self.buffer))
        else:
            last_transmissible_idx = min(self.last_sent + 1 + (self.max_buffer_size - self.packets_in_network),
                                         len(self.buffer))

        data_list = []
        for i in range(self.last_sent + 1, last_transmissible_idx):
            self.last_sent += 1
            data_list.append((self.last_sent, self.buffer[i]))
            self.packets_in_network += 1

        return data_list

    def set_ack_no(self, ack_no: int) -> None:
        """Sets ack number if it is what is expected"""
        if ack_no == self.last_successful_ack + 1:
            self.last_successful_ack = ack_no
            acks_processed = 0
            for ack in self.received_acks:
                if ack == self.last_successful_ack + 1:
                    self.last_successful_ack = ack
                    acks_processed += 1
            self.received_acks = self.received_acks[acks_processed:]

        else:
            self.received_acks.append(ack_no)
            self.received_acks.sort()
        self.packets_in_network -= 1

    def get_seq_no(self) -> int:
        return self.last_sent

    def all_data_acked(self) -> bool:
        return self.last_sent == self.last_successful_ack

    def get_data_from_seq_no(self, target) -> str:
        """Returns data of a particular seq no"""

        for seq, data in enumerate(self.buffer):
            if seq == target:
                return data
        return ""

    def get_retransmit_data(self, ack: int, SACK: list[int]) -> List[Packet]:
        """Gets allowable number packets between last ack that are not in SACK"""
        num_packets = self.max_buffer_size - self.packets_in_network + 1

        return_list = []

        for i in range(ack + 1, ack + num_packets):
            if i not in SACK:
                return_list.append((i, self.buffer[i]))

        return return_list

    def get_number_of_sendable_packets(self) -> int:
        """Returns number of packets that can be sent without filling the network"""
        return self.max_buffer_size - self.packets_in_network

    def additive_increase(self):
        """Increases window by 1"""
        log(f"Increasing window {self.max_buffer_size}")

    def multiplicative_decrease(self):
        """Decreases window by half"""
        log(f"Decreasing window: {self.max_buffer_size}")


if __name__ == "__main__":
    buf = SenderWindow(3)
