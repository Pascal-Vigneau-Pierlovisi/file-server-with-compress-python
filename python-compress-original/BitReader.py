import typing
from util import bytes_to_string


class BitReader:
    def __init__(self, fb: typing.BinaryIO, chunk_size: int):
        self.fb = fb
        self.chunk_size = chunk_size
        self.buffer = ""
        self.index = 0

    def read(self, amount: int) -> str:
        bits_left = len(self.buffer) - self.index

        if bits_left < amount:
            self.buffer = self.buffer[len(self.buffer) - bits_left :] + bytes_to_string(
                self.fb.read(self.chunk_size)
            )

        old_index = self.index
        self.index += amount

        return self.buffer[old_index : old_index + amount]