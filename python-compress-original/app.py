import os
import pickle
import zlib
from flask import Flask, render_template, request
import hauffman

app = Flask(__name__)

@app.route('/')
def index():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    return render_template('index.html', files=files)

@app.route('/compress', methods=['POST'])
def compress():
    file_path = request.form['file']
    compress_file(file_path)
    return 'File compressed successfully.'

@app.route('/decompress', methods=['POST'])
def decompress():
    file_path = request.form['file']
    decompress_file(file_path)
    return 'File decompressed successfully.'

def compress_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1

    root = hauffman.build_huffman_tree(frequencies)
    encoded_text, char_to_code = hauffman.encode_huffman(text, root)

    # Calculate padding
    padding_amount = 8 - len(encoded_text) % 8
    if padding_amount < 8:
        encoded_text += '0' * padding_amount

    # Write the encoded text and header to a binary file
    with open('compressed_data.bin', 'wb') as file:
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

def decompress_file(compressed_file_path):
    with open(compressed_file_path, 'rb') as file:
        # Read the length of the header (2 bytes)
        header_size_bytes = file.read(2)
        header_size = int.from_bytes(header_size_bytes, byteorder='big')

        # Read the header using the calculated size
        header_pickle = file.read(header_size)
        header = pickle.loads(header_pickle)

        # Read the encoded text
        encoded_text = file.read()

    root = hauffman.build_huffman_tree(header['frequencies'])
    decoded_text = hauffman.decode_huffman(''.join(f'{byte:08b}' for byte in encoded_text), root)

    with open('decompressed.txt', 'w') as file:
        file.write(decoded_text)

    print("Decompression completed. Decoded text saved to 'decompressed.txt'.")

if __name__ == '__main__':
    app.run(debug=True)