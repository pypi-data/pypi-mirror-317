# Run-Length Encoding


def encoder(content):
    if not content:
        return []
    # [(5, 3), (2, 2), (8, 4)] → [5, 5, 5, 2, 2, 8, 8, 8, 8]
    compressed_data = []

    prev = content[0]
    count = 1

    for curr in content[1:]:
        if curr == prev:
            count += 1
        else:
            compressed_data.append((prev, count))
            prev = curr
            count = 1
    return compressed_data + [(prev, count)]


def decoder(compressed_data):
    decompressed_data = []
    for char, count in compressed_data:
        decompressed_data += [char] * count
    return decompressed_data
