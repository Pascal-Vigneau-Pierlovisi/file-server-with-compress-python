from __future__ import annotations


class Node:
    def __init__(
        self,
        freq: int = -1,
        char: str = "",
        left: Node | None = None,
        right: Node | None = None,
    ):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, nxt: Node) -> bool:
        return self.freq < nxt.freq