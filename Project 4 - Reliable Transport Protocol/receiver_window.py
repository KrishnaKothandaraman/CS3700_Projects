from typing import Dict, List, Tuple, Set


class ReceiverWindow:
    """Class that mimics a memory buffer in C for TCP"""
    buffer: List[Tuple[int, str]]
    bufferedSequenceNos: Set[int]
    last_printed: int

    def __init__(self):
        self.buffer = []
        self.bufferedSequenceNos = set()
        self.last_printed = -1

    def add(self, seq_no: int, data: str) -> None:
        """Adds new data to the buffer before it's next packet. Builds buffer in ascending order of sequence numbers"""

        if self.already_buffered(seq_no):
            return

        insert_pos = -1
        for i, (seq, _) in enumerate(self.buffer):
            if seq > seq_no:
                insert_pos = i
                break
        if insert_pos == -1:
            self.buffer.append((seq_no, data))
        else:
            self.buffer.insert(insert_pos, (seq_no, data))

        self.bufferedSequenceNos.add(seq_no)

    def flush(self) -> List[Tuple[int, str]]:
        """Returns data from buffer that are valid"""
        return_list = []

        if not self.buffer:
            return []

        for seq, data in self.buffer:
            if seq == self.last_printed + 1:
                return_list.append((seq, data))
                self.last_printed += 1
            else:
                break
        self.buffer = self.buffer[len(return_list):]
        return return_list

    def already_buffered(self, seq_no: int) -> bool:
        """Returns True if seq_no is already in buffer. False otherwise"""
        return seq_no in self.bufferedSequenceNos

    def get_buffer_seq_nos(self) -> list[int]:
        """Returns sequence numbers of buffered data"""
        return list(map(lambda x: x[0], self.buffer))


if __name__ == "__main__":
    recv = ReceiverWindow()
    recv.add(0, "a")
    recv.add(3, "d")
    recv.add(2, "c")
    recv.add(1, "b")
    print(recv.get_buffer_seq_nos())

