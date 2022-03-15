import sys
from typing import Dict, List, Tuple, Set


def log(message):
    sys.stderr.write(message + "\n")
    sys.stderr.flush()


class ReceiverWindow:
    """Class that mimics a memory buffer in C for TCP"""
    buffer: List[Tuple[int, str]]
    bufferedSequenceNos: Set[int]

    def __init__(self):
        self.buffer = []
        self.bufferedSequenceNos = set()

    def add(self, seq_no: int, data: str) -> None:
        """Adds new data to the buffer before it's next packet. Builds buffer in ascending order of sequence numbers"""
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

    def flush(self, expectedSeqNo: int) -> Tuple[int, List[Tuple[int, str]]]:
        """Returns data from buffer that are valid"""
        return_list = []

        if not self.buffer:
            return -1, []
        # log(f"Current buffer: {self.buffer}")

        for seq, data in self.buffer:
            if seq == expectedSeqNo:
                return_list.append((seq, data))
                expectedSeqNo += 1
            else:
                break
        # log(f"New buffer: {self.buffer}")

        self.buffer = self.buffer[len(return_list):]

        if return_list:
            last_ordered_ack = return_list[-1][0]

        else:
            last_ordered_ack = expectedSeqNo
        return last_ordered_ack, return_list

    def already_buffered(self, seq_no: int) -> bool:
        """Returns True if seq_no is already in buffer. False otherwise"""
        return seq_no in self.bufferedSequenceNos

    def get_sack(self) -> List[int]:
        sack_list = []
        for seq_no, _ in self.buffer:
            sack_list.append(seq_no)

        return sack_list


if __name__ == "__main__":
    recv = ReceiverWindow()
    recv.add(1, "b")
    recv.add(2, "c")
    recv.add(0, "a")
    recv.add(5, "e")
    print(recv.flush())
    print(recv.buffer)
