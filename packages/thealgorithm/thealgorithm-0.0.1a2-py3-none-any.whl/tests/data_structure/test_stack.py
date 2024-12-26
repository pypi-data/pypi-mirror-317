import unittest
from thealgorithm.data_structure.stack import Stack


class TestStack(unittest.TestCase):

    def setUp(self):
        """Set up a new stack with a max size of 3 for each test."""
        self.stack = Stack(max_size=3)

    def test_push_within_limit(self):
        """Test pushing items within the size limit."""
        self.assertTrue(self.stack.push(1))
        self.assertTrue(self.stack.push(2))
        self.assertEqual(self.stack.size, 2)

    def test_push_beyond_limit(self):
        """Test pushing items beyond the size limit."""
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.assertFalse(self.stack.push(4))  # Should return False
        self.assertEqual(self.stack.size, 3)  # Size remains at max

    def test_pop(self):
        """Test popping items off the stack."""
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)  # LIFO behavior
        self.assertEqual(self.stack.size, 1)

    def test_pop_empty_stack(self):
        """Test popping from an empty stack returns None."""
        self.assertIsNone(self.stack.pop())

    def test_top(self):
        """Test retrieving the top item."""
        self.assertIsNone(self.stack.top())  # Empty stack should return None
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.top(), 2)  # Top should return the last pushed item

    def test_is_empty(self):
        """Test the is_empty method."""
        self.assertTrue(self.stack.is_empty())  # Should be empty initially
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())  # Should not be empty after push

    def test_size_property(self):
        """Test the size property."""
        self.assertEqual(self.stack.size, 0)
        self.stack.push(1)
        self.assertEqual(self.stack.size, 1)
        self.stack.push(2)
        self.assertEqual(self.stack.size, 2)
        self.stack.pop()
        self.assertEqual(self.stack.size, 1)


if __name__ == "__main__":
    unittest.main()
