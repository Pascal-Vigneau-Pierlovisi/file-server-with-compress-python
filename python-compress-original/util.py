from Node import Node


# Convert strings to bytes.
def string_to_bytes(data: str) -> bytes:
    b = bytearray()

    for i in range(0, len(data), 8):
        b.append(int(data[i : i + 8], 2))

    return bytes(b)


# Convert bytes to strings.
def bytes_to_string(bytes: bytes) -> str:
    return "".join(f"{n:08b}" for n in bytes)


# Convert trees into strings for testing purposes.
def tree_to_string(node: Node) -> str:
    if not node.left and not node.right:
        return node.char

    val = ""

    if node.left:
        val += "0" + tree_to_string(node.left)
    if node.right:
        val += "1" + tree_to_string(node.right)

    return val