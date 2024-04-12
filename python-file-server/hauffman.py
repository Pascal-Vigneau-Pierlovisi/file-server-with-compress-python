import pickle
from io import BytesIO

class TreeNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def build_huffman_tree(frequencies):
    nodes = [TreeNode(char, freq) for char, freq in frequencies.items()]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda node: node.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = TreeNode(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        nodes.append(parent)
    return nodes[0] if nodes else None

def encode_huffman(text, root):
    char_to_code = {}
    def traverse(node, code=""):
        if node is not None:
            if node.char is not None:
                char_to_code[node.char] = code
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
    traverse(root)

    encoded_text = ''.join(char_to_code[char] for char in text)
    return encoded_text, char_to_code

def compress(content):
    frequencies = {char: content.count(char) for char in set(content)}
    root = build_huffman_tree(frequencies)
    encoded_text, _ = encode_huffman(content, root)

    print("debug 41")

    padding = 8 - len(encoded_text) % 8
    encoded_text += '0' * padding

    encoded_bytes = bytearray(int(encoded_text[i:i+8], 2) for i in range(0, len(encoded_text), 8))

    print("debug 48")

    metadata = pickle.dumps((root, padding))
    compressed_file = BytesIO()
    # Écrire la taille du metadata (en supposant que cela reste sous 65535 octets, donc 2 octets suffisent)
    compressed_file.write(len(metadata).to_bytes(2, byteorder='big'))
    compressed_file.write(metadata)
    compressed_file.write(encoded_bytes)

    print("debug 57")
    # Déterminer la taille totale du contenu compressé
    compressed_file_size = compressed_file.tell()
    compressed_file.seek(0)

    print("debug 62")

    return compressed_file, compressed_file_size

def decode_huffman(encoded_text, root):
    decoded_text = ""
    node = root
    for bit in encoded_text:
        node = node.left if bit == '0' else node.right
        if node.char:
            decoded_text += node.char
            node = root
    return decoded_text

def decompress(compressed_file):
    metadata_size = int.from_bytes(compressed_file.read(2), byteorder='big')
    metadata = pickle.loads(compressed_file.read(metadata_size))
    root, padding = metadata
    encoded_bytes = compressed_file.read()
    encoded_text = ''.join(f'{byte:08b}' for byte in encoded_bytes)[:-padding]

    return decode_huffman(encoded_text, root)
