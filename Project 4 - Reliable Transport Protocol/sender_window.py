from typing import Dict, List, Tuple
import sys

Packet = Tuple[int, str]


def log(message):
    sys.stderr.write(message + "\n")
    sys.stderr.flush()


class SenderWindow:
    """Class that mimics a memory buffer in C for TCP"""
    buffer: List[str]
    last_sent: int
    last_ack: int
    max_buffer_size: int

    def __init__(self, max_buff):
        self.buffer = []
        self.last_sent = -1
        # normalize because last_sent starts at 0
        self.max_buffer_size = max_buff
        self.last_ack = -1
        self.sack = []

    def add_data(self, data: str) -> None:
        """Appends data to buffer"""
        self.buffer.append(data)

    def get_data_to_send(self) -> List[Packet]:
        """Gets all data that can be sent after taking into consideration packets that have been sent but are un
        acknowledged """

        # all data in buffer sent or network full
        if (self.last_sent + 1) > len(self.buffer) or (self.last_sent - self.last_ack) >= self.max_buffer_size:
            return []

        last_sliding_window_index = 0
        starting_index = 0
        if self.sack:
            last_sliding_window_index = self.sack[-1]
            starting_index = self.last_ack

        else:
            last_sliding_window_index = self.last_sent + (self.max_buffer_size - (self.last_sent - self.last_ack))
            starting_index = self.last_sent

        # minimum of last index in buffer or last index in the sliding window
        last_transmissible_idx = min(last_sliding_window_index + 1
                                     , len(self.buffer))

        data_list = []
        log("-------------------------------------")
        log(f"Buffer {self.buffer}")
        log(f"Sack: {self.sack}")
        log(f"Starting idx {starting_index + 1}")
        log(f"Ending idx {last_transmissible_idx}")
        log("-------------------------------------")

        for i in range(starting_index + 1, last_transmissible_idx):
            if i not in self.sack:
                self.last_sent = max(self.last_sent, i)
                data_list.append((self.last_sent, self.buffer[i]))

        return data_list

    def check_expected_ack_and_set(self, ack_no: int, sack: List[int]) -> None:
        """
        Checks if ack_no is expected. If expected, updates next expected ack. Otherwise, resets last sent index
        :param sack: Received sack
        :param ack_no: ack received
        """
        # TODO: Rethink last_ack logic because ack_no means everything until that packed has been received in order.
        # TODO: Question is how to infer from that, whether I need to retransmit a packet or not
        if ack_no == self.last_ack + 1:
            self.last_ack = ack_no
            self.sack = sack
        else:
            if sack:
                print(f"Resetting last ack to {self.last_ack}", flush=True)
                self.last_sent = self.last_ack
                self.sack = sack

    def get_seq_no(self) -> int:
        return self.last_sent

    def all_data_acked(self) -> bool:
        return self.last_sent == self.last_ack

    def get_data_by_sno(self, sno) -> str:
        for i, data in enumerate(self.buffer):
            if i == sno:
                return data
        return ""

    def reset_ack(self):
        self.last_sent = self.last_ack


if __name__ == "__main__":
    buf = SenderWindow(3)
    buf.add_data("a")
    buf.add_data("b")
    buf.add_data("c")
    print(buf.get_data_to_send())
    buf.check_expected_ack_and_set(0, [])
    buf.check_expected_ack_and_set(0, [2])
    print(buf.get_data_to_send())
    buf.check_expected_ack_and_set(2, [])
    print(buf.get_data_to_send())
