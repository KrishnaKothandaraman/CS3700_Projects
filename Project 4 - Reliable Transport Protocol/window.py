from typing import Dict, List, Tuple


class MemoryBuffer:
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
        self.last_ack = 0

    def add_data(self, data: str) -> None:
        """Appends data to buffer"""
        self.buffer.append(data)

    def get_data_to_send(self) -> List[Tuple[int,str]]:
        """Gets all data that can be sent after taking into consideration packets that have been sent but are un
        acknowledged """
        if (self.last_sent + 1) > len(self.buffer) or (self.last_sent - self.last_ack) >= self.max_buffer_size:
            return []

        if self.last_sent == -1:
            last_transmissible_idx = min(len(self.buffer), self.max_buffer_size)
        else:
            last_transmissible_idx = min(self.last_sent + (self.max_buffer_size - (self.last_sent - self.last_ack)) + 1
                                     , len(self.buffer))
        data_list = []
        for i in range(self.last_sent + 1, last_transmissible_idx):
            self.last_sent += 1
            data_list.append((self.last_sent, self.buffer[i]))

        return data_list

    def set_ack_no(self, ack_no: int) -> None:
        """Sets ack number"""
        self.last_ack = ack_no

    def get_seq_no(self) -> int:
        return self.last_sent

    def all_data_acked(self) -> bool:
        return self.last_sent == self.last_ack


if __name__ == "__main__":
    buf = MemoryBuffer(2)
    buf.add_data("0")
    buf.add_data("1")
    print(buf.get_data_to_send())
    buf.set_ack_no(1)
    buf.add_data("2")
    buf.add_data("3")
    print(buf.get_data_to_send())



