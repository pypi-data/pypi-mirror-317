from thealgorithm.data_compression.rle import decoder, encoder


def __test_encoder():
    raw = [5, 5, 5, 2, 2, 8, 8, 8, 8]
    expected = [(5, 3), (2, 2), (8, 4)]
    compressed = encoder(raw)
    assert compressed == expected, f"expect={expected}, got={compressed}"

    raw = [5, 5, 5, 2, 2, 8, 8, 8, 8, 9]
    expected = [(5, 3), (2, 2), (8, 4), (9, 1)]
    compressed = encoder(raw)
    assert compressed == expected, f"expect={expected}, got={compressed}"

    raw = [1, 2, 3]
    expected = [(1, 1), (2, 1), (3, 1)]
    compressed = encoder(raw)
    assert compressed == expected, f"expect={expected}, got={compressed}"

    raw = [1, 1, 1, 1, 1]
    expected = [(1, 5)]
    compressed = encoder(raw)
    assert compressed == expected, f"expect={expected}, got={compressed}"

    raw = []
    expected = []
    compressed = encoder(raw)
    assert compressed == expected, f"expect={expected}, got={compressed}"

    print("Passed")


def __test_decoder():
    compressed_data = [(5, 3), (2, 2), (8, 4)]
    expected = [5, 5, 5, 2, 2, 8, 8, 8, 8]
    decompressed = decoder(compressed_data)
    assert decompressed == expected, f"expect={expected}, got={decompressed}"

    compressed_data = [(5, 3), (2, 2), (8, 4), (9, 1)]
    expected = [5, 5, 5, 2, 2, 8, 8, 8, 8, 9]
    decompressed = decoder(compressed_data)
    assert decompressed == expected, f"expect={expected}, got={decompressed}"

    compressed_data = [(1, 1), (2, 1), (3, 1)]
    expected = [1, 2, 3]
    decompressed = decoder(compressed_data)
    assert decompressed == expected, f"expect={expected}, got={decompressed}"

    compressed_data = [(1, 5)]
    expected = [1, 1, 1, 1, 1]
    decompressed = decoder(compressed_data)
    assert decompressed == expected, f"expect={expected}, got={decompressed}"

    compressed_data = []
    expected = []
    decompressed = decoder(compressed_data)
    assert decompressed == expected, f"expect={expected}, got={decompressed}"

    print("Passed")
