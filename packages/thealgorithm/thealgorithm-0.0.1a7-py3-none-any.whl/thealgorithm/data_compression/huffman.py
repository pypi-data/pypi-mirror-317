from heapq import heappush, heappop
from collections import defaultdict


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def calculate_frequency(data):
    freq = defaultdict(int)
    for char in data:
        freq[char] += 1
    return freq


def build_tree(freq):
    heap = []
    for char, f in freq.items():
        heappush(heap, Node(char, f))

    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heappush(heap, merged)

    return heap[0] if heap else None


def build_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    if node is not None:
        if node.char is not None:
            codes[node.char] = prefix
        build_codes(node.left, prefix + "0", codes)
        build_codes(node.right, prefix + "1", codes)
    return codes


def encoder(data):
    if not data:
        return "", {}

    freq = calculate_frequency(data)
    root = build_tree(freq)
    codes = build_codes(root)
    encoded_data = "".join(codes[char] for char in data)
    return encoded_data, codes


def decoder(encoded_data, codes):
    if not encoded_data or not codes:
        return ""

    reverse_codes = {v: k for k, v in codes.items()}
    decoded_data = []
    current_code = ""
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codes:
            decoded_data.append(reverse_codes[current_code])
            current_code = ""

    return "".join(decoded_data)
