import pickle
from io import BytesIO


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_huffman_tree(frequencies):
    nodes = [TreeNode(char) for char, freq in frequencies.items()]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.value)
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = TreeNode(left.value + right.value)
        parent.left = left
        parent.right = right
        nodes.append(parent)
    return nodes[0]

def encode_huffman(text, root):
    encoded_text = ""
    char_to_code = {}

    def traverse(node, code=""):
        if node.left is None and node.right is None:
            char_to_code[node.value] = code
        if node.left:
            traverse(node.left, code + "0")
        if node.right:
            traverse(node.right, code + "1")

    traverse(root)

    for char in text:
        encoded_text += char_to_code[char]

    return encoded_text, char_to_code

def compress_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1

    root = build_huffman_tree(frequencies)
    encoded_text, char_to_code = encode_huffman(text, root)

    # Calculate padding
    padding_amount = 8 - len(encoded_text) % 8
    if padding_amount < 8:
        encoded_text += '0' * padding_amount

    # Write the encoded text and header to a binary file
    file = BytesIO()

    header = {'frequencies': frequencies, 'codes': char_to_code, 'padding': padding_amount}
    header_pickle = pickle.dumps(header)

    # Write the length of the header first (using 2 bytes)
    header_size = len(header_pickle).to_bytes(2, byteorder='big')
    file.write(header_size)

    # Write the header itself
    file.write(header_pickle)

    # Convert encoded text to bytes and write to file
    encoded_bytes = bytearray([int(encoded_text[i:i+8], 2) for i in range(0, len(encoded_text), 8)])

    file.write(encoded_bytes)

    print("Compression completed. Compressed data saved to 'compressed_data.bin'.")

    return file

# Example usage:
file_to_compress = 'test.txt'
#compress_file(file_to_compress)

import pickle

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_huffman_tree(frequencies):
    nodes = [TreeNode(char) for char, freq in frequencies.items()]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.value)
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = TreeNode(left.value + right.value)
        parent.left = left
        parent.right = right
        nodes.append(parent)
    return nodes[0]

def decode_huffman(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        elif bit == '1':
            current_node = current_node.right

        if current_node.left is None and current_node.right is None:
            decoded_text += current_node.value
            current_node = root

    return decoded_text

def decompress_file(file):
    #with open(compressed_file_path, 'rb') as file:
    # Read the length of the header (2 bytes)
    header_size_bytes = file.read(2)
    header_size = int.from_bytes(header_size_bytes, byteorder='big')

    # Read the header using the calculated size
    header_pickle = file.read(header_size)
    header = pickle.loads(header_pickle)

    # Read the encoded text
    encoded_text = file.read()

    root = build_huffman_tree(header['frequencies'])
    decoded_text = decode_huffman(''.join(f'{byte:08b}' for byte in encoded_text), root)

    with open('decompressed2222.txt', 'w') as file:
        file.write(decoded_text)

    print("Decompression completed. Decoded text saved to 'decompressed.txt'.")

# Example usage:
compressed_file_path = 'compressed_data.bin'
#decompress_file(compressed_file_path)
