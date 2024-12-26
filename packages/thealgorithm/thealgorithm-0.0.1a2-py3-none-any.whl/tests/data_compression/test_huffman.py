from thealgorithm.data_compression.huffman import encoder, decoder
import unittest


class TestHuffmanCoding(unittest.TestCase):
    def setUp(self):
        self.sample_text = "this is an example for huffman encoding"
        self.empty_text = ""
        self.double_char_text = "aabb"
        self.test_text = "hello world"

    def test_huffman_encoding(self):
        encoded_data, codes = encoder(self.sample_text)
        self.assertNotEqual(encoded_data, "")
        self.assertIsInstance(codes, dict)
        self.assertGreater(len(codes), 0)

    def test_huffman_decoding(self):
        encoded_data, codes = encoder(self.sample_text)
        decoded_data = decoder(encoded_data, codes)
        self.assertEqual(decoded_data, self.sample_text)

    def test_empty_text(self):
        encoded_data, codes = encoder(self.empty_text)
        self.assertEqual(encoded_data, "")
        self.assertEqual(codes, {})
        decoded_data = decoder(encoded_data, codes)
        self.assertEqual(decoded_data, "")

    def test_double_char_text(self):
        encoded_data, codes = encoder(self.double_char_text)
        decoded_data = decoder(encoded_data, codes)
        self.assertEqual(decoded_data, self.double_char_text)

    def test_general_case(self):
        encoded_data, codes = encoder(self.test_text)
        decoded_data = decoder(encoded_data, codes)
        self.assertEqual(decoded_data, self.test_text)
