# tests/test_module2.py

import unittest
from nnthvn.module2 import to_uppercase, reverse_string


class TestStringFunctions(unittest.TestCase):
    def test_to_uppercase(self):
        self.assertEqual(to_uppercase("hello"), "HELLO")
        self.assertEqual(to_uppercase("Hello"), "HELLO")
        self.assertEqual(to_uppercase("HELLO"), "HELLO")

    def test_reverse_string(self):
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string("abc"), "cba")
        self.assertEqual(reverse_string("racecar"), "racecar")  # Палиндром


if __name__ == "__main__":
    unittest.main()








