import unittest

from thealgorithm.sorting import quick


class TestQuickSort(unittest.TestCase):

    def test_ascending_order(self):
        arr = [45, 3, 17, 48, 72, 25, 8, 99, 14, 9, 12, 21, 81, 64, 33, 12]
        quick(arr, 0, len(arr) - 1, reverse=False)
        expected = [3, 8, 9, 12, 12, 14, 17, 21, 25, 33, 45, 48, 64, 72, 81, 99]
        self.assertEqual(arr, expected)

    def test_descending_order(self):
        arr = [45, 3, 17, 48, 72, 25, 8, 99, 14, 9, 12, 21, 81, 64, 33, 12]
        quick(arr, 0, len(arr) - 1, reverse=True)
        expected = [99, 81, 72, 64, 48, 45, 33, 25, 21, 17, 14, 12, 12, 9, 8, 3]
        self.assertEqual(arr, expected)

    def test_empty_list(self):
        arr = []
        quick(arr, 0, len(arr) - 1, reverse=False)
        self.assertEqual(arr, [])

    def test_single_element(self):
        arr = [42]
        quick(arr, 0, len(arr) - 1, reverse=False)
        self.assertEqual(arr, [42])

    def test_sorted_ascending(self):
        arr = [1, 2, 3, 4, 5]
        quick(arr, 0, len(arr) - 1, reverse=False)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_sorted_descending(self):
        arr = [5, 4, 3, 2, 1]
        quick(arr, 0, len(arr) - 1, reverse=True)
        self.assertEqual(arr, [5, 4, 3, 2, 1])


if __name__ == "__main__":
    unittest.main()
